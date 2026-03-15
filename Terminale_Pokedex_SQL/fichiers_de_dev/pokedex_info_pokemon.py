import pygame, sqlite3, os
from pygame.locals import *

# Connexion à la base de données
pokeBase = sqlite3.connect("pokeBase.db")
curseur = pokeBase.cursor()

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Pokedex de Kanto")
font = pygame.font.SysFont('Arial', 17)
pokeFont = pygame.font.Font('Fichiers_Sup/PKMN_RBYGSC.ttf', 20)

fleche_retour = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_retour = pygame.transform.scale(fleche_retour, (50, 30))
fleche_droite = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_droite = pygame.transform.scale(fleche_retour, (50, 30))
fleche_droite = pygame.transform.rotate(fleche_droite, -90)
fleche_gauche = pygame.image.load("Fichiers_Sup/fleche_retour.png")
fleche_gauche = pygame.transform.scale(fleche_retour, (50, 30))
fleche_gauche = pygame.transform.rotate(fleche_gauche, +90)
stats_bouton = pygame.image.load("Fichiers_Sup\Stats.png")
stats_bouton = pygame.transform.scale(stats_bouton, (50, 30))
stat = True
capacite_bouton = pygame.image.load("Fichiers_Sup\Capacite.png")
capacite_bouton = pygame.transform.scale(capacite_bouton, (50, 30))

running = True
rect_stats_bouton = stats_bouton.get_rect(topleft=(35, 265))
rect_capacite_bouton = capacite_bouton.get_rect(topleft=(150, 265))
rect_fleche_droite = fleche_droite.get_rect(topleft=(470, 225))
rect_fleche_gauche = fleche_gauche.get_rect(topleft=(0, 225))


class BoutonPok:
    def __init__(self, num, nom):
        self.numero = num
        self.nom = nom
        self.case = pygame.image.load("Fichiers_Sup/case.png")
        self.case = pygame.transform.scale(self.case, (496, 496))
        self.rect = self.case.get_rect()
        self.rect.topleft = (2, 2)
        self.n = 0
        self.visible = True
        self.clickable = False
        self.compteur = 0
        self.intervalle_animation = 8
        self.capacites = []

        #charge les sprites animes
        self.sprites = self.charger_sprites(num)
        self.sprite_index = 0
        self.t = 10

        #charge les sprites animes
        self.sprites = self.charger_sprites(num)
        self.sprite_index = 0
        self.t = 10

        self.scroll_offset = 1
        self.scroll_limit = len(self.capacites) * 25

        # Informations
        curseur.execute("SELECT Informations FROM Description WHERE IdDescription = ?", (num,))
        resultat = curseur.fetchone()
        self.info = resultat[0] if resultat else "Aucune information disponible."

        # Catégorie
        curseur.execute("SELECT Categorie FROM Description WHERE IdDescription = ?", (num,))
        resultat_cat = curseur.fetchone()
        self.categorie = resultat_cat[0] if resultat_cat else "Inconnue"

        # Poids
        curseur.execute("SELECT Poids FROM Description WHERE IdDescription = ?", (num,))
        resultat_poid = curseur.fetchone()
        self.poids = resultat_poid[0] if resultat_poid else "N/A"

        # Taille
        curseur.execute("SELECT Taille FROM Description WHERE IdDescription = ?", (num,))
        resultat_taille = curseur.fetchone()
        self.taille = resultat_taille[0] if resultat_taille else "N/A"

        # Stats
        curseur.execute("SELECT PV,ATK,DEF,ATKSPE,DEFSPE,VIT FROM Stats  WHERE IdStats = ?",  (num,))
        PV,ATK,DEF,ATKSPE,DEFSPE,VIT = curseur.fetchone()
        self.PV = PV
        self.ATK = ATK
        self.DEF = DEF
        self.ATKSPE = ATKSPE
        self.DEFSPE = DEFSPE
        self.VIT = VIT

        # Capacités
        curseur.execute("""
                        SELECT Capacité,Types.Nom,Puissance,Precision,Catégorie 
                        FROM Attaques 
                            JOIN CapacitePokemon 
                                ON Attaques.IdCapacité = CapacitePokemon.IdCapacité 
                            JOIN Types
                                ON Attaques.Type = Types.IdType
                        WHERE NumPokedex = ?"""
                        ,  (num,))
        Capacité = curseur.fetchall()
        for capacite in Capacité:
            attaque = {
                "Nom": capacite[0],
                "Type": capacite[1],
                "Puissance": capacite[2],
                "Précision": capacite[3],
                "Catégorie": capacite[4]
            }
            self.capacites.append(attaque)
    
    
    def charger_sprites(self, num):
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

    def afficher_texte(self, surface, texte, position, font, couleur, largeur_max):
        mots = texte.split()
        lignes = []
        ligne_actuelle = ""

        for mot in mots:
            test_ligne = ligne_actuelle + " " + mot if ligne_actuelle else mot
            if font.size(test_ligne)[0] <= largeur_max:
                ligne_actuelle = test_ligne
            else:
                lignes.append(ligne_actuelle)
                ligne_actuelle = mot

        lignes.append(ligne_actuelle)

        x, y = position
        for ligne in lignes:
            surface.blit(font.render(ligne, True, couleur), (x, y))
            y += font.get_height()

    def affichage(self):
        if self.visible:
            screen.blit(self.case, (self.rect.x, self.rect.y))

            # Numéro et nom
            num = pokeFont.render(self.numero, True, 'Black')
            screen.blit(num, (170, 40))
            nom = pokeFont.render(self.nom, True, 'Black')
            screen.blit(nom, (270, 40))

            # Informations
            titre_info = font.render("Information du Pokédex:", True, 'Black')
            screen.blit(titre_info, (30, 185))
            self.afficher_texte(screen, self.info, (40, 210), font, 'Black', 440)

            # Catégorie
            titre_categorie = font.render("Catégorie:", True, 'Black')
            screen.blit(titre_categorie, (170, 85))
            categorie = font.render(self.categorie, True, 'Black')
            screen.blit(categorie, (260, 85))

            # Poids
            titre_poids = font.render("Poids:", True, 'Black')
            screen.blit(titre_poids, (170, 105))
            poids_valeur = font.render(f"{self.poids} g", True, 'Black')
            screen.blit(poids_valeur, (260, 105))

            # Taille
            titre_taille = font.render("Taille:", True, 'Black')
            screen.blit(titre_taille, (170, 125))
            taille_valeur = font.render(f"{self.taille} cm", True, 'Black')
            screen.blit(taille_valeur, (260, 125))

            # Stats
            if stat == True:
                titre_PV = font.render("PV:", True, 'Green')
                screen.blit(titre_PV, (50, 300))
                PV_valeur = font.render(f"{self.PV}", True, 'Black')
                screen.blit(PV_valeur, (170, 300))

                titre_ATK = font.render("Attaque:", True, 'Red')
                screen.blit(titre_ATK, (50 , 320))
                ATK_valeur = font.render(f"{self.ATK}", True, 'Black')
                screen.blit(ATK_valeur, (170, 320))

                titre_DEF = font.render("Défense:", True, 'Purple')
                screen.blit(titre_DEF, (50, 340))
                DEF_valeur = font.render(f"{self.DEF}", True, 'Black')
                screen.blit(DEF_valeur, (170, 340))

                titre_ATKSPE = font.render("Attaque spécial:", True, 'Red')
                screen.blit(titre_ATKSPE, (50, 360))
                ATKSPE_valeur = font.render(f"{self.ATKSPE}", True, 'Black')
                screen.blit(ATKSPE_valeur, (170, 360))

                titre_DEFSPE = font.render("Défense spécial:", True, 'Purple')
                screen.blit(titre_DEFSPE, (50, 380))
                DEFSPE_valeur = font.render(f"{self.DEFSPE}", True, 'Black')
                screen.blit(DEFSPE_valeur, (170, 380))

                titre_VIT = font.render("Vitesse:", True, 'Blue')
                screen.blit(titre_VIT, (50, 400))
                VIT_valeur = font.render(f"{self.VIT}", True, 'Black')
                screen.blit(VIT_valeur, (170, 400))

            # Capacité

            if not stat:
                height_limit = 287
    
                y_offset = 300 - self.scroll_offset 

                for capacite in self.capacites:
                    
                    texte_capacite1 = f"{capacite['Nom']} | Type: {capacite['Type']} | Catégorie: {capacite['Catégorie']}"
                    texte_capacite2 = f"Puissance: {capacite['Puissance']} | Précision: {capacite['Précision']}"
                    capacite_render1 = font.render(texte_capacite1, True, 'Black')
                    capacite_render2 = font.render(texte_capacite2, True, 'Black')

                    
                    if y_offset > height_limit:  
                        screen.blit(capacite_render1, (20, y_offset))
                        screen.blit(capacite_render2, (20, y_offset + 25))
                        pygame.draw.rect(screen, (0, 0, 0), (18, y_offset, 350, 50), 1)

                    
                    y_offset += 50  

            # Sprite
            n_sprite = len(self.sprites)
            self.compteur += 1
            if self.compteur >= self.intervalle_animation:
                self.sprite_index = (self.sprite_index + 1) % n_sprite
                self.compteur = 0
            image = pygame.image.load("Sprites_Animés/" + self.sprites[self.sprite_index])
            image = pygame.transform.scale(image, (140, 140))
            screen.blit(image, (20, 40))

            # Cadre
            pygame.draw.rect(screen, (0, 0, 0), (20, 40, 140, 140), 5)  # Noir
            pygame.draw.rect(screen, (192, 192, 192), (23, 43, 134, 134), 3)  # Gris
            pygame.draw.rect(screen, (255, 255, 255), (25, 45, 130, 130), 2)  # Blanc

def rechercherNom(texte):
    requete = "SELECT NumPokedex, Nom FROM Pokemon WHERE Nom LIKE ?"
    curseur.execute(requete, [f"%{texte}%"])
    return curseur.fetchall()

listeNoms = [elt[1] for elt in rechercherNom("")]
listeBouton = []
for i in range(1, 152):
    num = f'{i:04}'
    listeBouton.append(BoutonPok(num, listeNoms[i - 1], ))
index_actuel = 1

while running:
    screen.fill((137, 228, 230))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  
                if listeBouton[index_actuel - 1].scroll_offset > -1000000000000000000000000000000:
                    listeBouton[index_actuel - 1].scroll_offset += 25
            elif event.button == 5:  
                if listeBouton[index_actuel - 1].scroll_offset < 10000000000000000000000000000000:
                    listeBouton[index_actuel - 1].scroll_offset -= 25
            if rect_fleche_droite.collidepoint(event.pos):
                if index_actuel < 151:
                    index_actuel += 1
            if rect_fleche_gauche.collidepoint(event.pos): 
                if index_actuel > 1:
                    index_actuel -= 1
            if rect_stats_bouton.collidepoint(event.pos):
                stat = True
            if rect_capacite_bouton.collidepoint(event.pos):
                stat = False

    listeBouton[index_actuel - 1].affichage()
    screen.blit(fleche_retour, (230, 0))
    screen.blit(stats_bouton, rect_stats_bouton.topleft)
    screen.blit(capacite_bouton, rect_capacite_bouton.topleft)
    if index_actuel > 1:
        screen.blit(fleche_gauche, rect_fleche_gauche.topleft)
    if index_actuel < 151:
        screen.blit(fleche_droite, rect_fleche_droite.topleft)

    pygame.display.flip()