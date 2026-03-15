import pygame, sqlite3, os
from pygame.locals import *

pokeBase = sqlite3.connect("pokeBase.db")
curseur = pokeBase.cursor()

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pokedex de Kanto")

# Initialisation de certaines images
carre=pygame.image.load("Fichiers_Sup/carre.png")
carre=pygame.transform.scale(carre, (500, 500))
fleche_retour = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_retour = pygame.transform.scale(fleche_retour, (50, 30))
fleche_droite = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_droite = pygame.transform.scale(fleche_retour, (50, 30))
fleche_droite = pygame.transform.rotate(fleche_droite, -90)
fleche_gauche = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_gauche = pygame.transform.scale(fleche_retour, (50, 30))
fleche_gauche = pygame.transform.rotate(fleche_gauche, +90)
rect_fleche_droite = fleche_droite.get_rect(topleft=(470, 225))
rect_fleche_gauche = fleche_gauche.get_rect(topleft=(0, 225))
rect_fleche_retour= fleche_retour.get_rect(topleft=(230, 0))
stats_bouton = pygame.image.load("Fichiers_Sup/Stats.png")
stats_bouton = pygame.transform.scale(stats_bouton, (50, 30))
stat = True
capacite_bouton = pygame.image.load("Fichiers_Sup/Capacite.png")
capacite_bouton = pygame.transform.scale(capacite_bouton, (50, 30))
rect_stats_bouton = stats_bouton.get_rect(topleft=(35, 265))
rect_capacite_bouton = capacite_bouton.get_rect(topleft=(150, 265))

font = pygame.font.SysFont('Arial', 15)
pokeFont = pygame.font.Font('Fichiers_Sup/PKMN_RBYGSC.ttf', 20)
running = True
ecriture = True
texte = ""
pagePokedex=False

colonne="NumPokedex"
tri="ASC"

# Gestion des animations
index_actuel=0
compteur=0
sprite_index=0
spriteAnim=[]

# Gestion du scroll
scrollY = 0
scrollY2 = 0 
scrollSpeed = 50 
buttonHeight = 100 
maxScroll = 0  

class Timer:
    """Permet de patienter afin d'effectuer une action sans arrêter le programme."""
    def __init__(self):
        self.valeur = 0
        self.sauvegardé = False
        self.valeurBloqué = 0

    def ajouté(self):
        """Ajoute 1 au timer à la fin de la boucle."""
        self.valeur += 1

    def reset(self):
        """Remet le timer à 0."""
        self.valeur = 0
        self.sauvegardé = False
        self.valeurBloqué = 0

    def bloquerValeur(self):
        """Garde en mémoire une valeur."""
        if self.sauvegardé == False:
            self.valeurBloqué = self.valeur
            self.sauvegardé = True

    def augmenterValeurBloquée(self, nb):
        """Augmenter la valeur sauvegardée d'un certain nombre."""
        self.valeurBloqué += nb

    def tempsPassé(self, temps):
        """Compare si un laps de temps donné est passé entre le timer et la valeur bloquée."""
        return self.valeurBloqué == self.valeur - temps

class BoutonPok:
    """Bouton permettant l'accès à la page pokédex du pokémon concerné."""
    def __init__(self, num, nom, miniatures, posX, posY):
        self.numero=num
        self.nom=nom
        self.case=pygame.image.load("Fichiers_Sup/case.png")
        self.listeImg=miniatures
        self.rect=self.case.get_rect()
        self.rect.topleft=(posX, posY)
        self.coorDefault=(posX, posY)
        self.n=0
        self.visible=True
        self.clickable=False
        self.estCliqué=False
        self.timer=Timer()

    def affichage(self):
        """Affiche le bouton avec le nom, le numéro et une image animée du pokémon."""
        screen.blit(self.case,(self.rect.x,self.rect.y))
        num = pokeFont.render(self.numero,True,'Black')
        screen.blit(num,(self.rect.x+100,self.rect.y+40))
        nom = pokeFont.render(self.nom,True,'Black')
        screen.blit(nom,(self.rect.x+200,self.rect.y+40))
        self.timer.bloquerValeur()
        minia=pygame.image.load(self.listeImg[self.n])
        minia=pygame.transform.scale(minia,(90,90))
        screen.blit(minia,(self.rect.x,self.rect.y))
        self.timer.ajouté()
        if self.timer.tempsPassé(30):
            self.n=(self.n+1)%2
            self.timer.reset()

    def utilisation(self):
        """Détecte si le bouton est cliqué si il peut être cliqué."""
        mousePos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]==1 and not self.estCliqué and self.clickable:
                self.estCliqué=True
        return self.estCliqué

class Bouton:
    def __init__(self,cheminImg,posX,posY):
        self.img=pygame.image.load(cheminImg)
        self.rect=self.img.get_rect()
        self.rect.topleft=(posX,posY)
        self.estCliqué=False

    def utilisation(self,autreBoutons=None):
        """Détecte si l'utilisateur clique sur le bouton pour l'activer.
        Détecte si l'utilisateur appuie ailleurs pour désactiver le bouton.
        Si une liste de boutons est renseignée, le bouton ne se désactivera pas si l'on appuie sur ces boutons."""
        screen.blit(self.img,self.rect.topleft)
        mousePos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]==1 and not self.estCliqué:
                self.estCliqué=True
        elif pygame.mouse.get_pressed()[0]==1 and self.estCliqué:
            if autreBoutons==None:
                self.estCliqué=False
            else:
                verif=True
                for bouton in autreBoutons:
                    if bouton.rect.collidepoint(mousePos):
                        verif=False
                if verif:
                    self.estCliqué=False

class Capa:
    def __init__(self,nom,type,puissance,précision,catégorie,methode,x,décal):
        self.nom=nom
        self.type=type
        self.puissance=puissance
        self.précision=précision
        self.catégorie=catégorie
        self.methode=methode
        self.visible=False
        self.case = pygame.image.load("Fichiers_Sup/case.png")
        self.case = pygame.transform.scale(self.case, (500, 25))
        self.x=x
        self.décal=décal

    def affichage(self,scrollY):
        """Affiche les capacités selon le scrollY, si la capacité se trouve dans la fenêtre d'intervalle défini."""
        posY=scrollY+self.décal+300
        if posY<=250 or posY>=450:
            self.visible=False
        else:
            self.visible=True
        
        texte_capacite1 = f"{self.nom} | Type: {self.type} | Catégorie: {self.catégorie}"
        texte_capacite2 = f"Puissance: {self.puissance} | Précision: {self.précision} | Méthode: {self.methode}"
        capacite_render1 = font.render(texte_capacite1, True, 'Black')
        capacite_render2 = font.render(texte_capacite2, True, 'Black')

        if self.visible:
            screen.blit(capacite_render1, (self.x,posY))
            screen.blit(capacite_render2, (self.x,posY+25))
            pygame.draw.rect(screen, (0, 0, 0), (18, posY, 350, 50), 1)

def taperTexte(texte):
    """Détecte les touches pressé par l'utilisateur et ajoute leurs valeurs dans la variable texte ou éxecute une action leur étant propre avant de renvoyer la variable."""
    listeElt = ["à", "&", "é", '"', "'", "(", "-", "è", "_", "ç"]
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            texte = texte[:-1] # Retire un élément
        elif event.key == pygame.K_DELETE:
            texte = "" # Réinitialise la variable
        elif event.key in [pygame.K_PAGEUP,pygame.K_PAGEDOWN,pygame.K_RETURN, pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_TAB, pygame.K_CAPSLOCK, pygame.K_ESCAPE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            pass # Ne fait rien
        elif event.key == pygame.K_SPACE:
            texte += " "
        elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
            texte += listeElt[int(pygame.key.name(event.key))] 
        else:
            texte += pygame.key.name(event.key)
        return texte

def rechercherNom(texte):
    """Recherche dans la base de données si un nom de pokémon correspond à la variable renseignée et renvoie la liste des pokémon.
    La variable colonne et tri modifie l'ordre de la liste."""
    requete = f"SELECT NumPokedex, Nom FROM Pokemon WHERE Nom LIKE ? ORDER BY {colonne} {tri}"
    curseur.execute(requete, [f"%{texte}%"])
    resultat = curseur.fetchall()
    return resultat

def affichageBoutons(listeTempo):
    """Affiche à l'écran les boutons se trouvant dans listeTempo si ils se trouvent dans la fenêtre les uns en dessous des autres et les rend clickable."""
    n=0
    for pokeNom in listeTempo:
        for i in range(len(listeBouton)):
            if pokeNom==listeBouton[i].nom:
                listeBouton[i].visible=True
                listeBouton[i].rect.y=50+n*100+scrollY #augmente ou dimminue sa mosition en lien avec le scroll
                if listeBouton[i].rect.y>-50 and listeBouton[i].rect.y<500 and listeBouton[i].visible: #si les bouton dépasse une certaine position alors ils deviennent inclicable
                    listeBouton[i].affichage()
                    if listeBouton[i].rect.y>=50:
                        listeBouton[i].clickable=True
                    else:
                        listeBouton[i].clickable=False
        n+=1
    for bouton in listeBouton:
        if bouton.nom not in listeTempo:
            bouton.visible=False
def chercherType(num): 
    """"La fonction cherche les types du pokemon afficher.
        Si le pokemon n'a que Type 1, le resultat sera null donc on recherche juste le type 1."""
    curseur.execute("""
                    SELECT Type1.Nom,Type2.Nom 
                    FROM Pokemon 
                        JOIN Types AS Type1 
                            ON Pokemon.Type1=Type1.IdType 
                        JOIN Types AS Type2 
                            ON Pokemon.Type2=Type2.IdType 
                    WHERE NumPokedex = ?""", [num])
    resultat = curseur.fetchall()
    if len(resultat)==0: # Le pokemon n'a qu'un type donc resultat est null
        curseur.execute("""
                        SELECT Type1.Nom 
                        FROM Pokemon 
                            JOIN Types AS Type1 
                                ON Pokemon.Type1=Type1.IdType 
                        WHERE NumPokedex = ?""", [num])
        resultat = curseur.fetchall()
    return resultat[0]
    
def chercherInfo(num,index):
    """Recherche les informations du pokemon d'index num et renvoie l'info se trouvant à la position index."""
    curseur.execute("SELECT * FROM Description WHERE IdDescription = ?", (num,))
    resultat = curseur.fetchall()
    resultat = resultat[0][index]
    return resultat

def chercherStats(num,index):
    """Recherche les stats du pokemon d'index num et renvoie l'info se trouvant à la position index."""
    curseur.execute("SELECT PV,ATK,DEF,ATKSPE,DEFSPE,VIT FROM Stats  WHERE IdStats = ?",  (num,))
    resultat = curseur.fetchall()
    resultat = resultat[0][index]
    return resultat

def chercherEvo(num,coordonnees):
    """Recherche si le pokemon d'index num possède une évolution et affiche aux coordonnees données le nom de l'évolution et sa méthode d'évolution."""
    curseur.execute("SELECT Nom,Niveau,Description FROM Evolution JOIN MethodesEvo ON Evolution.Methode=MethodesEvo.IdMethode JOIN Pokemon ON Evolution.NumEvolution=Pokemon.NumPokedex WHERE NumBase = ?", (num,))
    resultat=curseur.fetchall()
    if len(resultat)==0:
        t=font.render("Pas d'evolution",True,'Black')
        screen.blit(t,coordonnees)
    else:
        x,y=coordonnees
        for i in range(len(resultat)):
            t=font.render(f"Evolue en {resultat[i][0]}",True,'Black')
            if resultat[i][1]==None:
                t2=font.render(f"Methode : {resultat[i][2]}",True,'Black')
            else:
                t2=font.render(f"Au niveau {resultat[i][1]}",True,'Black')
            screen.blit(t,(x,y))
            screen.blit(t2,(x,y+20))
            y+=45

def chercherCapa(num):
    """ Cherche les capacitées du pokemon dans le SQL et met les données dans un dictionnaire 
    qui contient les infos sur une capacité que l'on transforme en Objet de classe 
    que l'on ajoute dans une liste a chaque nouvelle capacité puis on renvoie cette liste."""
    listeCapa=[]
    curseur.execute("""
                    SELECT Capacité,Types.Nom,Puissance,Precision,Catégorie,MethodesApprentissage.Methode
                    FROM Attaques 
                        JOIN CapacitePokemon 
                            ON Attaques.IdCapacité = CapacitePokemon.IdCapacité 
                        JOIN Types
                            ON Attaques.Type = Types.IdType
                        JOIN MethodesApprentissage
                            ON MethodesApprentissage.IdMethode=CapacitePokemon.Methode
                    WHERE NumPokedex = ?"""
                    ,  (num,))
    capacité = curseur.fetchall()
    i=0
    for elt in capacité:
        attaque = {
            "Nom": elt[0],
            "Type": elt[1],
            "Puissance": elt[2],
            "Précision": elt[3],
            "Catégorie": elt[4],
            "Methode":elt[5]
        }

        listeCapa.append(Capa(attaque["Nom"],attaque["Type"],attaque["Puissance"],attaque["Précision"],attaque["Catégorie"],attaque["Methode"],20,i*50))
        i+=1
    return listeCapa


def charger_sprites(num):
    """Récupère les images composant l'animation du pokemon numéro num, les tri dans l'ordre et renvoie la liste."""
    sprites_folder = "Sprites_Animés"
    poke_sprites={}
    for file in os.listdir(sprites_folder):
        if num in file:
            nombre = file[-6:-4]
            if nombre[0] == "_":
                nombre = nombre[1:]
            nombre = int(nombre)
            poke_sprites[nombre]=file
    return [poke_sprites[key] for key in sorted(poke_sprites.keys())]

def afficher_texte(surface, texte, position, font, couleur, largeur_max):
    """Fonction permettant de revenir à la ligne si le texte dépasse une largeur max et affiche ce texte."""
    mots = texte.split()   #mots devient la longeur du text (le nombre de mot)
    lignes = []
    ligne_actuelle = ""

    for mot in mots:   
        test_ligne = ligne_actuelle + " " + mot if ligne_actuelle else mot # le texte va prendre en compte la position y de la ligne puis on compte les espaces sans couper les mots
        if font.size(test_ligne)[0] <= largeur_max: #si le texte dépasse la limite imposer alors on revient à la ligne
            ligne_actuelle = test_ligne
        else:   #sinon on continue à poser les mots à la suite sans revenir à la ligne
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot

    lignes.append(ligne_actuelle)

    x, y = position
    for ligne in lignes:  #Cela permet de gérer l'espacement entre les lignes tout en les affichant
        surface.blit(font.render(ligne, True, couleur), (x, y))
        y += font.get_height()  

listeNoms = [elt[1] for elt in rechercherNom("")]  
listeBouton = []
for i in range(1, 152):
    if i < 10:
        listeBouton.append(BoutonPok(f'000{i}', listeNoms[i - 1], [f'Miniatures/Miniature_000{i}_0.png', f'Miniatures/Miniature_000{i}_1.png'], 0, 50))
    elif i < 100:
        listeBouton.append(BoutonPok(f'00{i}', listeNoms[i - 1], [f'Miniatures/Miniature_00{i}_0.png', f'Miniatures/Miniature_00{i}_1.png'], 0, 50))
    else:
        listeBouton.append(BoutonPok(f'0{i}', listeNoms[i - 1], [f'Miniatures/Miniature_0{i}_0.png', f'Miniatures/Miniature_0{i}_1.png'], 0, 50))

boutonFiltre = Bouton("Fichiers_Sup/filtre.png", 450, 0)
boutonNom=Bouton("Fichiers_Sup/nom.png",425,50)
boutonNum=Bouton("Fichiers_Sup/num.png",425,100)
boutonCroissant=Bouton("Fichiers_Sup/croissant.png",425,150)
boutonDecroissant=Bouton("Fichiers_Sup/decroissant.png",425,200)
boutonMenu=[boutonNom,boutonNum,boutonCroissant,boutonDecroissant]

while running:
    screen.fill((137, 228, 230))
    
    if not pagePokedex:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Texte
            if ecriture:
                texteTempo=taperTexte(texte)
                if texteTempo!=None:
                    texte=texteTempo

                if event.type == pygame.MOUSEBUTTONDOWN: # Détecte si un bouton de la souris est pressé
                    if event.button == 4:  # Molette vers le haut
                        scrollY += scrollSpeed 
                    elif event.button == 5: # Molette vers le bas
                        scrollY -= scrollSpeed  

                if event.type==pygame.KEYDOWN: # Fonctionne de la même manière que les lignes au-dessus mais pour les flèches
                    if event.key==pygame.K_UP:
                        scrollY+=scrollSpeed 
                    elif event.key==pygame.K_DOWN:
                        scrollY-=scrollSpeed  
                    elif event.key==pygame.K_PAGEUP:
                        scrollY=0
                    elif event.key==pygame.K_PAGEDOWN:
                        scrollY=-maxScroll

                for i in range(len(listeBouton)):
                    if listeBouton[i].visible and not pagePokedex:
                        pagePokedex=listeBouton[i].utilisation()
                        index_actuel=i+1
        
        if scrollY > 0: # Empêche de sortir des limites de la liste afficher
            scrollY = 0
        if scrollY < -maxScroll:
            scrollY = -maxScroll 
        
        listeTempo = [elt[1] for elt in rechercherNom(texte)]
        listeNom=[elt[1] for elt in rechercherNom(texte)]
        maxScroll = max(0, len(listeTempo) * buttonHeight - screen.get_height()+50)
        affichageBoutons(listeTempo)

        # Affichage du texte
        barre = pygame.image.load("Fichiers_Sup/barre.png")
        barre = pygame.transform.scale(barre, (450, 50))
        screen.blit(barre, (0, 0))
        imageTexte = font.render(texte, True, 'Black')
        screen.blit(imageTexte, (15, 15))
        
        # Boutons
        boutonFiltre.utilisation(boutonMenu)
        if boutonFiltre.estCliqué:
            boutonNom.utilisation()
            if boutonNom.estCliqué:
                colonne="Nom"
            boutonNum.utilisation()
            if boutonNum.estCliqué:
                colonne="NumPokedex"
            boutonCroissant.utilisation()
            if boutonCroissant.estCliqué:
                tri="ASC"
            boutonDecroissant.utilisation()
            if boutonDecroissant.estCliqué:
                tri="DESC"
            for bouton in listeBouton:
                bouton.clickable=False
            ecriture=False
        else:
            ecriture=True

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Molette de la souris vers le bas
                        scrollY2 += 50
                elif event.button == 5:  # Molette de la souris vers le haut
                        scrollY2 -= 50
                if rect_fleche_droite.collidepoint(event.pos):
                    if index_actuel < len(listeBouton):
                        index_actuel += 1
                        spriteAnim=[]
                        sprite_index=0
                if rect_fleche_gauche.collidepoint(event.pos): 
                    if index_actuel > 1:
                        index_actuel -= 1
                        spriteAnim=[]
                        sprite_index=0
                if rect_fleche_retour.collidepoint(event.pos):
                    pagePokedex=False
                    for bouton in listeBouton:
                        bouton.estCliqué=False
                if rect_stats_bouton.collidepoint(event.pos):
                    stat = True
                if rect_capacite_bouton.collidepoint(event.pos):
                    stat = False

        listeCapa=chercherCapa(index_actuel)
        maxCapa=len(listeCapa) * 50-150
        if scrollY2 > 0: # Empêche de sortir des limites de la liste afficher
            scrollY2 = 0
        if scrollY2 < -maxCapa:
            scrollY2 = -maxCapa 

        screen.blit(carre,(0,0))
        if spriteAnim==[]:
            spriteAnim=charger_sprites(listeBouton[index_actuel-1].numero)

        # Sprite
        n_sprite = len(spriteAnim)
        compteur += 1
        if compteur >= 3:
            sprite_index = (sprite_index + 1) % n_sprite
            compteur = 0
        image = pygame.image.load("Sprites_Animés/" + spriteAnim[sprite_index])
        image=pygame.transform.scale(image,(140,140))
        screen.blit(image, (20, 40))

        # Numéro et nom
        num = pokeFont.render(str(index_actuel), True, 'Black')
        screen.blit(num, (170, 40))
        curseur.execute("SELECT Nom FROM Pokemon WHERE NumPokedex = ?",(index_actuel,))
        resultat=curseur.fetchall()
        nom=resultat[0][0]
        nom = pokeFont.render(nom, True, 'Black')
        screen.blit(nom, (270, 40))

        chercherEvo(index_actuel,(320, 85))

        # Informations
        info=chercherInfo(index_actuel,4)
        titre_info = font.render("Information du Pokédex:", True, 'Black')
        screen.blit(titre_info, (30, 200))
        afficher_texte(screen, info, (50, 225), font, 'Black', 400)

        # Catégorie
        categorie=chercherInfo(index_actuel,1)
        titre_categorie = font.render("Catégorie:", True, 'Black')
        screen.blit(titre_categorie, (170, 85))
        categorie = font.render(categorie, True, 'Black')
        screen.blit(categorie, (230, 85))

        # Poids
        poids=chercherInfo(index_actuel,3)
        titre_poids = font.render("Poids:", True, 'Black')
        screen.blit(titre_poids, (170, 105))
        poids_valeur = font.render(f"{poids/1000} kg", True, 'Black')
        screen.blit(poids_valeur, (230, 105))

        # Taille
        taille=chercherInfo(index_actuel,2)
        titre_taille = font.render("Taille:", True, 'Black')
        screen.blit(titre_taille, (170, 125))
        taille_valeur = font.render(f"{taille/100} m", True, 'Black')
        screen.blit(taille_valeur, (230, 125))

        type=chercherType(index_actuel)
        # Type
        if len(type)==1:
            titre_Type = font.render("Type:", True, 'Black')
            screen.blit(titre_Type, (170, 145))
            Type_valeur = font.render(f"{type[0]}", True, 'Black')
            screen.blit(Type_valeur, (230, 145))
        else:
            titre_Type1 = font.render("Type 1:", True, 'Black')
            screen.blit(titre_Type1, (170, 145))
            Type1_valeur = font.render(f"{type[0]}", True, 'Black')
            screen.blit(Type1_valeur, (230, 145))
            titre_Type2 = font.render("Type 2:", True, 'Black')
            screen.blit(titre_Type2, (170, 165))
            Type2_valeur = font.render(f"{type[1]}", True, 'Black')
            screen.blit(Type2_valeur, (230, 165))

        # Stats
        if stat:
            titre_PV = font.render("PV:", True, 'Green')
            screen.blit(titre_PV, (25, 300))
            PV_valeur = font.render(f"{chercherStats(index_actuel,0)}", True, 'Black')
            screen.blit(PV_valeur, (125, 300))
            
            titre_ATK = font.render("Attaque:", True, 'Red')
            screen.blit(titre_ATK, (25, 320))
            ATK_valeur = font.render(f"{chercherStats(index_actuel,1)}", True, 'Black')
            screen.blit(ATK_valeur, (125, 320))
            
            titre_DEF = font.render("Defence:", True, 'Purple')
            screen.blit(titre_DEF, (25, 340))
            DEF_valeur = font.render(f"{chercherStats(index_actuel,2)}", True, 'Black')
            screen.blit(DEF_valeur, (125, 340))
            
            titre_ATKSPE = font.render("Attaque spécial:", True, 'Red')
            screen.blit(titre_ATKSPE, (25, 360))
            ATKSPE_valeur = font.render(f"{chercherStats(index_actuel,3)}", True, 'Black')
            screen.blit(ATKSPE_valeur, (125, 360))

            titre_DEFSPE = font.render("Defence spécial:", True, 'Purple')
            screen.blit(titre_DEFSPE, (25, 380))
            DEFSPE_valeur = font.render(f"{chercherStats(index_actuel,4)}", True, 'Black')
            screen.blit(DEFSPE_valeur, (125, 380))

            titre_VIT = font.render("Vitesse:", True, 'Blue')
            screen.blit(titre_VIT, (25, 400))
            VIT_valeur = font.render(f"{chercherStats(index_actuel,5)}", True, 'Black')
            screen.blit(VIT_valeur, (125, 400))

        # Capacités
        else:
            for capa in listeCapa:
                capa.affichage(scrollY2)

        # Cadre
        pygame.draw.rect(screen, (0, 0, 0), (20, 40, 140, 140), 5)  # Noir
        pygame.draw.rect(screen, (192, 192, 192), (23, 43, 134, 134), 3)  # Gris
        pygame.draw.rect(screen, (255, 255, 255), (25, 45, 130, 130), 2)

        screen.blit(fleche_retour, rect_fleche_retour.topleft)
        screen.blit(stats_bouton, rect_stats_bouton.topleft)
        screen.blit(capacite_bouton, rect_capacite_bouton.topleft)
        if index_actuel > 1:
            screen.blit(fleche_gauche, rect_fleche_gauche.topleft)
        if index_actuel < len(listeBouton):
            screen.blit(fleche_droite, rect_fleche_droite.topleft)

        if not pagePokedex:
            spriteAnim=[]
            compteur=0
            sprite_index=0
    pygame.display.flip()

pygame.quit()