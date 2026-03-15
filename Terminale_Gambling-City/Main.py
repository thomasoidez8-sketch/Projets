import pygame
from pygame.locals import *
from random import *
from sources.events import get_events
import sources.Blackjack as Blackjack,sources.Baccara as Baccara,sources.Bank as Bank,sources.Machine_à_sous as Machine_à_sous,sources.Roulette as Roulette,sources.Gestion_saves as Gestion_saves,sources.Succes as Succes,sources.Enchere as Enchere,sources.Goblets as Goblets,sources.Boite as Boite,time

# Création de la fenêtre
pygame.init()
pygame.mixer.init()

clock=pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
icon=pygame.image.load("data/icone.ico")
pygame.display.set_icon(icon)
pygame.display.set_caption("Gambling city")

# Initialisation des arrières-plans
menu=pygame.image.load("data/textures_menu/menu.png")
hall=pygame.image.load("data/textures_menu/hall.png")
ville=pygame.image.load("data/textures_menu/ville.png")
tableBlackjack=pygame.image.load("data/textures_blackjack/Table_blackjack.png")
tableBaccara=pygame.image.load("data/table_baccara.png")
bankBackground=pygame.image.load("data/textures_bank/Bank.png")
machine = pygame.image.load("data/textures_machine_à_sous/background.png")
plateauRoulette = pygame.image.load("data/texture_roulette/plateaux.png")
fond_gobelets = pygame.image.load("data/texture_gobelet/plateaux_jeux_gobelet.png")
fond_gobelets = pygame.transform.scale(fond_gobelets, (1000, 600))
bar = pygame.image.load("data/textures_succes/bar.png")
scène_allumée=pygame.image.load("data/textures_enchères/enchere_allume.png")
barreJoueur=pygame.image.load("data/textures_enchères/barreVente.png")
fondRect=pygame.Surface((500,150))
fondRect.fill((255,255,255))
fondRect.set_alpha(80)
# Charger l'image du pop-up
image_popup = pygame.image.load("data/textures_enchères/image_popup.png")
image_popup = pygame.transform.scale(image_popup, (800, 400))

police=pygame.font.Font('data/fichiers_additionnels/Crang.ttf',16)
petitePolice=pygame.font.Font('data/fichiers_additionnels/Crang.ttf',11)
police2=pygame.font.Font('data/fichiers_additionnels/MinecraftStandard.otf',25)

logo=pygame.image.load("data/textures_menu/logo.png")
bourse=pygame.image.load("data/textures_menu/bourse.png")

# Initialisation des musiques
musiqueMenu="data/fichiers_additionnels/roues_et_jetons.mp3"
musiqueCasino="data/fichiers_additionnels/casino_theme.mp3"
musiqueEnchère="data/fichiers_additionnels/enchère_theme.wav"
musiqueVille="data/fichiers_additionnels/ville_theme.wav"

musiqueActuelle=""

# Variables
sauvegarde = Gestion_saves.Gestion_sauvegarde()
sauvegarde.load()
bourseJetons = sauvegarde.bourseJetons
Bank.dette = sauvegarde.dette
Enchere.listeAchat=Gestion_saves.loadOeuvre()
Enchere.listePerte=Gestion_saves.loadOeuvrePerdu()
lieu="menu"
jeuSelectionné="menu"
running = True
indexMaison=0
oeuvreVente=None
img=None

# Classe
class BoutonJeux(Blackjack.Bouton):
    def survoler(self,screen):
        mousePos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            return self.utilisation(screen)

# Fonctions
def changementEcran(bouton,jeu,module):
    """Permet de passer d'un jeu à un autre."""
    global jeuSelectionné
    if Blackjack.actionBouton==jeu and not bouton.boutonEnfonce:
        Blackjack.actionBouton=""
        jeuSelectionné=jeu
        transfertJetons(module)

def transfertJetons(module):
    """Permet de synchroniser le nombre de jetons d'un jeu au menu."""
    global bourseJetons
    if jeuSelectionné=="menu":
        bourseJetons=module.jetonsDisponibles+module.mise
        module.jetonsDisponibles=0
        module.mise=0
    else:
        module.jetonsDisponibles=bourseJetons
        bourseJetons=0

def modifierMusique(musique):
    """Change la musique actuelle par la musique spécifiée."""
    global musiqueActuelle
    if musiqueActuelle!=musique:
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        musiqueActuelle=musique

# Instanciation des classes
boutonJouer=Blackjack.Bouton("hall","data/textures_menu/boutonJouer.png",600,175)
boutonSauvegarde=Blackjack.Bouton("save","data/textures_menu/sauvegarde.png",600,425)
boutonReset=Blackjack.Bouton("reset","data/textures_menu/reset.png",725,425)

boutonBlackjack=BoutonJeux("blackjack","data/textures_menu/boutonBlackjack.png",230,364)
boutonBaccara=BoutonJeux("baccara","data/textures_menu/boutonBaccara.png",642,364)
boutonMenuRoulette=BoutonJeux("roulette","data/textures_menu/boutonRoulette.png",596,286)
boutonMachine=BoutonJeux("machine","data/textures_menu/boutonMachine.png",230,272)
boutonEnchere=BoutonJeux("enchere","data/textures_menu/fleche_enchere.png",425,250)
boutonBank=Blackjack.Bouton("bank","data/textures_menu/boutonBank.png",849,275)
boutonVille=BoutonJeux("ville","data/textures_menu/fleche_ville.png",425,500)
boutonCasino=BoutonJeux("hall","data/textures_menu/fleche_casino.png",350,525)
boutonMaison=BoutonJeux("maison","data/textures_menu/fleche_maison.png",155,250)
boutonSucces=Blackjack.Bouton("prize","data/textures_menu/boutonPrize.png",49,275)

boutonGobelets=BoutonJeux("gobelets","data/textures_menu/boutonGobelets.png",861,384)
boutonBoite=BoutonJeux("boite","data/textures_menu/boutonBoiteMystere.png",394,287)
boutonFlecheGauche=Blackjack.Bouton(-1,"data/textures_bank/fleche_gauche.png",405,500)
boutonAnnuler=Blackjack.Bouton("annuler","data/textures_bank/annuler.png",405+boutonFlecheGauche.image.get_width(),500)
boutonFlecheDroite=Blackjack.Bouton(1,"data/textures_bank/fleche_droite.png",405+boutonFlecheGauche.image.get_width()+boutonAnnuler.image.get_width(),500)

boutonMenu=Blackjack.Bouton("menu","data/textures_menu/boutonMenu.png",460,15,"data/bouton_sombre/boutonMenu_sombre.png")

succes_1 = Succes.Succes("data/textures_succes/SDF.png",100,70,2)
succes_2 = Succes.Succes("data/textures_succes/blackjack_tropher.png",200,70,2)
succes_3 = Succes.Succes("data/textures_succes/trophe.png",300,70,2)
succes_4 = Succes.Succes("data/textures_succes/roulette_tropher.png",400,70,2)
succes_5 = Succes.Succes("data/textures_succes/baccara_tropher.png",500,70,2)
succes_6 = Succes.Succes("data/textures_succes/riche_tropher.png",600,70,2)
succes_7 = Succes.Succes("data/textures_succes/fan_art_tropher.png",700,70,2)
succes_8 = Succes.Succes("data/textures_succes/goblet_tropher.png",800,70,2)

requete="""SELECT IdOeuvre FROM Oeuvres ORDER BY Importance"""
Enchere.curseur.execute(requete)
for tableau in Enchere.curseur.fetchall():
    ajout=True
    i=tableau[0]
    for element in Enchere.listeAchat:
        if element['id']==i:
            ajout=False
    for element in Enchere.listePerte:
        if element==i:
            ajout=False
    if ajout:
        Enchere.listeOeuvre.append(Enchere.Oeuvre(i,screen))

Blackjack.constitutionPioche(Blackjack.listesCartes)    # Pioche du Blackjack
for i in range(8):                                      # Pioche du Baccara
    Blackjack.constitutionPioche(Baccara.listeCarte)

# Boucle infinie
while running:
    events = get_events()
    for event in events:
        if event.type == pygame.QUIT: # Arrête le programme si le joueur ferme la fenêtre
            running = False

    if Bank.dette >= 1500:
        succes_1.gagner = True
    if Blackjack.blackjack:
        succes_2.gagner = True
    if Machine_à_sous.spin.jackpot:
        succes_3.gagner = True
    if Roulette.vert:
        succes_4.gagner = True
    if Baccara.egaliter:
        succes_5.gagner = True
    if bourseJetons >= 100000:
        succes_6.gagner = True
    if len(Enchere.listeAchat) == 22:
        succes_7.gagner = True
    else:
        succes_7.gagner = False 
    if Goblets.vitesse_max:
        succes_8.gagner = True

    if lieu=="menu":
        screen.blit(menu,(0,0))
        screen.blit(logo,(99,33))
        modifierMusique(musiqueMenu)
        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonJouer.utilisation(screen))
        if Blackjack.actionBouton=="hall" and not boutonJouer.boutonEnfonce:
            Blackjack.actionBouton=""
            lieu="hall"
        succes_1.gagner = sauvegarde.succes_1
        succes_2.gagner = sauvegarde.succes_2
        succes_3.gagner = sauvegarde.succes_3
        succes_4.gagner = sauvegarde.succes_4
        succes_5.gagner = sauvegarde.succes_5
        succes_6.gagner = sauvegarde.succes_6
        succes_7.gagner = sauvegarde.succes_7
        succes_8.gagner = sauvegarde.succes_8

        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonSauvegarde.utilisation(screen))
        if Blackjack.actionBouton=="save" and not boutonSauvegarde.boutonEnfonce:
            sauvegarde.save()
            for oeuvre in Enchere.listeAchat:
                Gestion_saves.saveOeuvre(oeuvre)
            for id in Enchere.listePerte:
                Gestion_saves.saveOeuvrePerdu(id)
        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonReset.utilisation(screen))
        if Blackjack.actionBouton=="reset" and not boutonReset.boutonEnfonce:
            sauvegarde.reset()
            bourseJetons = sauvegarde.bourseJetons
            Bank.dette = sauvegarde.dette
            # ajouter init des succes
        
            Blackjack.blackjack=False
            Baccara.egaliter=False
            Goblets.vitesse_max=False
            Roulette.vert=False

    elif lieu=="hall":
        if jeuSelectionné=="menu":
            screen.blit(hall,(0,0))
            
            modifierMusique(musiqueCasino)
            # Retour au menu
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                (sauvegarde.bourseJetons,sauvegarde.dette,
                 sauvegarde.succes_1,sauvegarde.succes_2,sauvegarde.succes_3,
                 sauvegarde.succes_4,sauvegarde.succes_5,sauvegarde.succes_6,
                 sauvegarde.succes_7,sauvegarde.succes_8) = bourseJetons,Bank.dette,succes_1.gagner,succes_2.gagner,succes_3.gagner,succes_4.gagner,succes_5.gagner,succes_6.gagner,succes_7.gagner,succes_8.gagner
                lieu="menu"
            # Bouton Blackjack
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonBlackjack.survoler(screen))
            changementEcran(boutonBlackjack,"blackjack",Blackjack)
            # Bouton Baccara
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonBaccara.survoler(screen))
            changementEcran(boutonBaccara,"baccara",Baccara)
            # Bouton Roulette
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenuRoulette.survoler(screen))
            changementEcran(boutonMenuRoulette,"roulette",Roulette)
            # Bouton Machine à sous
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMachine.survoler(screen))
            changementEcran(boutonMachine,"machine",Machine_à_sous)
            # Bouton Enchères
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonEnchere.survoler(screen))
            changementEcran(boutonEnchere,"enchere",Enchere)
            if oeuvreVente!=None:
                Enchere.listeOeuvre.insert(0,oeuvreVente)
                oeuvreVente=None
            # Bouton Banque
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonBank.utilisation(screen))
            if Blackjack.actionBouton=="bank" and not boutonBank.boutonEnfonce:
                Blackjack.actionBouton=""
                jeuSelectionné="bank"
                Bank.jetonsDisponibles=bourseJetons
                bourseJetons=0
                Bank.action=None
            # Bouton Bar
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonSucces.utilisation(screen))
            if Blackjack.actionBouton=="prize" and not boutonSucces.boutonEnfonce:
                Blackjack.actionBouton=""
                jeuSelectionné="prize"
            # Bouton Ville
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonVille.survoler(screen))
            if Blackjack.actionBouton=="ville" and not boutonVille.boutonEnfonce:
                Blackjack.actionBouton=""
                lieu="ville"

            screen.blit(bourse,(850,25))
            Blackjack.affichageTexte(str(bourseJetons),police,860,70,"brown",screen)

        elif jeuSelectionné=="blackjack":
            screen.blit(tableBlackjack,(0,0))

            if Blackjack.commencerPartie==False:
                Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
                changementEcran(boutonMenu,"menu",Blackjack)

                Blackjack.preparation(screen,Blackjack.listeJetons)

            elif Blackjack.commencerPartie==True:
                boutonMenu.affichage_sombre(screen)
                Blackjack.tourJoueur(screen,tableBlackjack,police)         

            Blackjack.affichages(screen,police)    

        elif jeuSelectionné=="baccara":
            screen.blit(tableBaccara,(0,0))

            # Affichage des variables
            Blackjack.affichageTexte(str(Baccara.jetonsDisponibles),police,145,45,'brown',screen)
            Blackjack.affichageTexte(str(Baccara.mise),police,825,45,'brown',screen)
            
            # Affichage du jeu de cartes de l'utilisateur
            Baccara.jeuJoueur.affichage(screen)
            Baccara.jeuJoueur.calculValeur()
            Blackjack.affichageTexte(f"Valeur du jeu : {Baccara.jeuJoueur.valeurJeu}",police2,85,300,'white',screen)
            # Affichage du jeu de cartes de la banque
            Baccara.jeuBank.affichage(screen)
            Baccara.jeuBank.calculValeur()
            Blackjack.affichageTexte(f"Valeur du jeu : {Baccara.jeuBank.valeurJeu}",police2,580,300,'white',screen)

            if not Baccara.commencerPartie:
                Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
                changementEcran(boutonMenu,"menu",Baccara)

                Baccara.partie(screen)
            elif Baccara.commencerPartie:
                boutonMenu.affichage_sombre(screen)
                Baccara.finPartie(Baccara.jeuJoueur,Baccara.jeuBank,screen)

        elif jeuSelectionné=="bank":
            screen.blit(bankBackground,(0,0))
            # Retour au emnu
            if not Bank.endetté:
                Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
                if Blackjack.actionBouton=="menu" and not boutonMenu.boutonEnfonce:
                    Blackjack.actionBouton=""
                    jeuSelectionné="menu"
                    bourseJetons=Bank.jetonsDisponibles
                    Bank.jetonsDisponibles=0

                # Affichage des variables
                Blackjack.affichageTexte(str(Bank.jetonsDisponibles),police,155,30,'brown',screen)
                Blackjack.affichageTexte(str(Bank.dette),police,810,30,'brown',screen)

                Bank.boutonRembourser.valeur=Bank.dette

                if Bank.action=="vendreOeuvre":
                    if Bank.indexVente!=0:
                        Blackjack.affichageTexte(listeVente[Bank.indexVente]['nom'],petitePolice,400,540,'white',screen)
                        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonVendre.utilisation(screen))
                        if Blackjack.actionBouton=="vendre" and not Bank.boutonVendre.boutonEnfonce:
                            oeuvreVendue=listeVente.pop(Bank.indexVente)
                            Bank.indexVente=0
                            for i in range(len(Enchere.listeAchat)):
                                if not Bank.venteConclu:
                                    if oeuvreVendue['id']==Enchere.listeAchat[i]['id']:
                                        Enchere.listeAchat.pop(i)
                                        Enchere.listePerte.append(oeuvreVendue['id'])
                                        indexMaison=0
                                        Bank.venteConclu=True
                                    
                            Bank.jetonsDisponibles+=oeuvreVendue['prix']//2
                            Blackjack.actionBouton=None

                    else:
                        Bank.venteConclu=False
                        Blackjack.affichageTexte(listeVente[Bank.indexVente],petitePolice,400,540,'white',screen)
                    Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonFlecheGauche.utilisation(screen))
                    if Blackjack.actionBouton==-1 and not Bank.boutonFlecheGauche.boutonEnfonce:
                        if Bank.indexVente>0:
                            Bank.indexVente-=1
                            Blackjack.actionBouton=None
                    Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonFlecheDroite.utilisation(screen))
                    if Blackjack.actionBouton==1 and not Bank.boutonFlecheDroite.boutonEnfonce:
                        if Bank.indexVente<len(listeVente)-1:
                            Bank.indexVente+=1
                            Blackjack.actionBouton=None
                    Bank.boutonVendre.affichage(screen)
                    if Bank.boutonAnnuler.utilisation(screen)=="annuler":
                        Bank.action=None
                else:
                    # Emprunt
                    if Bank.jetonsDisponibles==0:
                        if Bank.action=="emprunt":
                            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonEmprunt100.utilisation(screen))
                            Bank.emprunt(Bank.boutonEmprunt100.valeur)
                            Blackjack.affichageTexte("Max : 2000",police,445,540,'white',screen)
                            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonEmprunt500.utilisation(screen))
                            Bank.emprunt(Bank.boutonEmprunt500.valeur)
                            if Bank.jetonsDisponibles!=0:
                                Bank.action=None
                        else:
                            Bank.boutonRembourser.affichage_sombre(screen)
                            Bank.action=Blackjack.associationBoutonVariable(Bank.action,Bank.boutonEmprunter.utilisation(screen))
                    # Remboursement
                    elif Bank.dette!=0 and Bank.jetonsDisponibles>=Bank.dette:
                        Bank.boutonEmprunter.affichage_sombre(screen)
                        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Bank.boutonRembourser.utilisation(screen))
                        Bank.remboursement(Bank.boutonRembourser.valeur)
                    # Ni l'un, ni l'autre
                    else:
                        Bank.boutonEmprunter.affichage_sombre(screen)
                        Bank.boutonRembourser.affichage_sombre(screen)
                    
                    if Bank.action!="emprunt":
                        Bank.action=Blackjack.associationBoutonVariable(Bank.action,Bank.boutonVendreOeuvre.utilisation(screen))
                        Bank.indexVente=0
                        listeVente=["Aucune"]+Enchere.listeAchat

            running=Bank.expulsion(screen,running,sauvegarde)
        
        elif jeuSelectionné=="machine":
            screen.blit(machine,(0,0))
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))  # Bouton pour revenir au menu
            # Affiche le trophée si l'utilisateur décroche le jackpot
            if Machine_à_sous.spin.jackpot == True:
                Machine_à_sous.win.afficher()
            
            # Affichage et utilisation du bouton spin
            Machine_à_sous.spin.affichage()
            Machine_à_sous.spin.clic(events)
            # Utilisation des jetons
            Machine_à_sous.jeton1.utilisation(events)
            Machine_à_sous.jeton5.utilisation(events)
            Machine_à_sous.jeton25.utilisation(events)
            Machine_à_sous.jeton50.utilisation(events)
            Machine_à_sous.jeton100.utilisation(events)
            Machine_à_sous.jeton500.utilisation(events)
            Machine_à_sous.jetonAllIn.utilisation(events)
            Machine_à_sous.jetonAllIn.valeur=Machine_à_sous.jetonsDisponibles
            # Affichage des roues de la machine
            Machine_à_sous.roue1.affichage()
            Machine_à_sous.roue2.affichage()
            Machine_à_sous.roue3.affichage()
            # Affichage des textes
            Machine_à_sous.affichageTexte(str(Machine_à_sous.jetonsDisponibles),police,145,45,'brown')
            Machine_à_sous.affichageTexte(str(Machine_à_sous.mise),police,825,45,'brown')
            changementEcran(boutonMenu,"menu",Machine_à_sous)
        
        elif jeuSelectionné=="roulette":
            screen.blit(plateauRoulette,(0,0))
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
            changementEcran(boutonMenu,"menu",Roulette)

            Blackjack.affichageTexte(str(Roulette.jetonsDisponibles),police,145,45,'brown',screen)
            Blackjack.affichageTexte(str(Roulette.mise),police,825,45,'brown',screen)
            Blackjack.affichageTexte(" ".join(str(v) for v in Roulette.paris.values()), police, 580, 400, 'brown', screen)
            
            # Tourner la roulette
            screen.blit(Roulette.coque_roulette,(49,175))
            Roulette.boutonRoulette.utilisation(screen)
            Roulette.boutonRoulette.tourner_roulette(screen)
            Roulette.boutonRoulette.afficher_resultat(screen)
            # Utilisation des jetons
            Roulette.jeton1.utilisation(screen)
            Roulette.jeton5.utilisation(screen)
            Roulette.jeton25.utilisation(screen)
            Roulette.jeton50.utilisation(screen)
            Roulette.jeton100.utilisation(screen)
            Roulette.jeton500.utilisation(screen)
            Roulette.jetonAllIn.valeur=Roulette.jetonsDisponibles
            Roulette.jetonAllIn.utilisation(screen)
            # Utilisation des boutons des numéros
            Roulette.bouton_numero_0.utilisation(screen)
            Roulette.bouton_numero_1.utilisation(screen)
            Roulette.bouton_numero_2.utilisation(screen)
            Roulette.bouton_numero_3.utilisation(screen)
            Roulette.bouton_numero_4.utilisation(screen)
            Roulette.bouton_numero_5.utilisation(screen)
            Roulette.bouton_numero_6.utilisation(screen)
            Roulette.bouton_numero_7.utilisation(screen)
            Roulette.bouton_numero_8.utilisation(screen)
            Roulette.bouton_numero_9.utilisation(screen)
            Roulette.bouton_numero_10.utilisation(screen)
            Roulette.bouton_numero_11.utilisation(screen)
            Roulette.bouton_numero_12.utilisation(screen)
            Roulette.bouton_numero_13.utilisation(screen)
            Roulette.bouton_numero_14.utilisation(screen)
            Roulette.bouton_numero_15.utilisation(screen)
            Roulette.bouton_numero_16.utilisation(screen)
            Roulette.bouton_numero_17.utilisation(screen)
            Roulette.bouton_numero_18.utilisation(screen)
            Roulette.bouton_numero_19.utilisation(screen)
            Roulette.bouton_numero_20.utilisation(screen)
            Roulette.bouton_numero_21.utilisation(screen)
            Roulette.bouton_numero_22.utilisation(screen)
            Roulette.bouton_numero_23.utilisation(screen)
            Roulette.bouton_numero_24.utilisation(screen)
            Roulette.bouton_numero_25.utilisation(screen)
            Roulette.bouton_numero_26.utilisation(screen)
            Roulette.bouton_numero_27.utilisation(screen)
            Roulette.bouton_numero_28.utilisation(screen)
            Roulette.bouton_numero_29.utilisation(screen)
            Roulette.bouton_numero_30.utilisation(screen)
            Roulette.bouton_numero_31.utilisation(screen)
            Roulette.bouton_numero_32.utilisation(screen)
            Roulette.bouton_numero_33.utilisation(screen)
            Roulette.bouton_numero_34.utilisation(screen)
            Roulette.bouton_numero_35.utilisation(screen)
            Roulette.bouton_numero_36.utilisation(screen)
            # Utilisation des boutons des intervalles
            Roulette.bouton_intervalle_1_12.utilisation(screen)
            Roulette.bouton_intervalle_13_24.utilisation(screen)
            Roulette.bouton_intervalle_25_36.utilisation(screen)
            Roulette.bouton_intervalle_1_to_18.utilisation(screen)
            Roulette.bouton_colonne_1.utilisation(screen)
            Roulette.bouton_colonne_2.utilisation(screen)
            Roulette.bouton_colonne_3.utilisation(screen)
            Roulette.bouton_colonne_even.utilisation(screen)
            Roulette.bouton_colonne_rouge.utilisation(screen)
            Roulette.bouton_colonne_noire.utilisation(screen)
            Roulette.bouton_colonne_odd.utilisation(screen)
            Roulette.bouton_intervalle_19_to_36.utilisation(screen)

        elif jeuSelectionné=="enchere":
            if not Enchere.vente:
                modifierMusique(musiqueCasino)
                screen.blit(hall,(0,0))
                screen.blit(bourse,(850,25))
                boutonBank.affichage(screen)
                boutonSucces.affichage(screen)
                Blackjack.affichageTexte(str(Enchere.jetonsDisponibles),police,860,70,"brown",screen)
                pygame.draw.rect(screen,(255,255,255),(250, 225, 500, 150), 3)
                screen.blit(fondRect,(250,225))
                if len(Enchere.listeOeuvre)>0 or oeuvreVente!=None:
                    if oeuvreVente==None:
                        oeuvreVente=Enchere.listeOeuvre.pop(0)
                        coursVente=oeuvreVente.prix
                    if Enchere.jetonsDisponibles<coursVente:
                        Blackjack.affichageTexte("Vous n'avez pas assez d'argent !",police,280,250,'white',screen)
                        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Enchere.retour.utilisation(screen))
                        changementEcran(Enchere.retour,"menu",Enchere)
                        if oeuvreVente!=None:
                            Enchere.listeOeuvre.insert(0,oeuvreVente)
                            oeuvreVente=None
                    else:
                        Blackjack.affichageTexte("Souhaitez-vous commencer une vente ?",police,280,250,'white',screen)

                        if Enchere.oui.utilisation(screen)=='Oui':
                            Enchere.oui.clickable=False
                            Enchere.non.clickable=False

                        Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Enchere.non.utilisation(screen))
                        changementEcran(Enchere.non,"menu",Enchere)
                    

                    if not Enchere.oui.clickable :
                        for place in Enchere.listePlace:
                            place.desattribution()
                        listeAcheteur=[]
                        Enchere.dernierAcheteur=None
                        tempsJoueur=5
                        screen.blit(Enchere.scène,(0,0))
                        Enchere.organisation(oeuvreVente.nbAcheteur)
                        Enchere.vente=True
                        jetonsBase=Enchere.jetonsDisponibles
                        for place in Enchere.listePlace:
                            if place.occupé:
                                listeAcheteur.append(place.occupant)
                                place.occupant.seuilAchat(coursVente,oeuvreVente.importance)
                        nbAcheteur=len(listeAcheteur)

                else:
                    Blackjack.affichageTexte("Tout a été vendu !",police,280,250,'white',screen)
                    Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,Enchere.retour.utilisation(screen))
                    changementEcran(Enchere.retour,"menu",Enchere)

            elif Enchere.vente:
                modifierMusique(musiqueEnchère)
                screen.blit(Enchere.scène,(0,0))
                screen.blit(oeuvreVente.image,oeuvreVente.rect.topleft)
                Enchere.jetonsDisponibles=jetonsBase-coursVente

                for place in Enchere.listePlace:
                    if place.occupé:
                        place.occupant.affichage(screen)

                if tempsJoueur>0:
                    if Enchere.dernierAcheteur=="joueur":
                        Enchere.vente=False
                        infosOeuvre={'id':oeuvreVente.id,'nom':oeuvreVente.nom,'artiste':oeuvreVente.artiste,'musée':oeuvreVente.musée,'image':Enchere.nomImg(oeuvreVente.nom),'prix':coursVente,'tailleImg':(oeuvreVente.image.get_width(),oeuvreVente.image.get_height())}
                        Enchere.listeAchat.append(infosOeuvre)
                        Enchere.mise=0
                        oeuvreVente=None
                        # Assombrir l'écran
                        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 180))
                        screen.blit(overlay, (0, 0))

                        popup_x = (screen.get_width() - image_popup.get_width()) // 2
                        popup_y = (screen.get_height() - image_popup.get_height()) // 2
                        screen.blit(image_popup, (popup_x, popup_y))

                        message = "Félicitations ! Vous avez gagné !"
                        couleur = "green"

                        Blackjack.affichageTexte(message, police, popup_x+225, popup_y+210, couleur, screen)
                        pygame.display.flip()

                        attendre = True
                        while attendre:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                                    attendre = False
                    else:
                        Enchere.timerJoueur.bloquerValeur()
                        screen.blit(barreJoueur,(323,490))
                        Blackjack.affichageTexte(str(tempsJoueur),police,664,492,'black',screen)
                        for bouton in Enchere.listeBouton:
                            proposition=Enchere.mise
                            choixJoueur=bouton.utilisation(screen,Enchere.jetonsDisponibles,Enchere.mise)
                            if choixJoueur!=None:
                                Enchere.dernierAcheteur="joueur"
                                Enchere.jetonsDisponibles,Enchere.mise=choixJoueur[0],choixJoueur[1]
                                proposition=Enchere.mise-proposition
                                coursVente+=proposition
                                tempsJoueur=0
                                Enchere.timerJoueur.reset()

                        if Enchere.timerJoueur.tempsPassé(60):
                            tempsJoueur-=1
                            Enchere.timerJoueur.reset()
                        x=nbAcheteur

                else:
                    Enchere.timerJoueur.bloquerValeur()
                    if x<nbAcheteur:
                        listeAcheteur[x].affichageBulle(screen)
                    if x>0 and Enchere.timerJoueur.tempsPassé(60):
                        if Enchere.dernierAcheteur==listeAcheteur[x-1]:
                            Enchere.vente=False
                            Enchere.jetonsDisponibles=jetonsBase
                            Enchere.mise=0
                            Enchere.listePerte.append(oeuvreVente.id)
                            oeuvreVente=None
                            # Assombrir l'écran
                            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                            overlay.fill((0, 0, 0, 180))
                            screen.blit(overlay, (0, 0))

                            popup_x = (screen.get_width() - image_popup.get_width()) // 2
                            popup_y = (screen.get_height() - image_popup.get_height()) // 2
                            screen.blit(image_popup, (popup_x, popup_y))

                            message = "Dommage. Vous avez perdu..."
                            couleur = "red"

                            Blackjack.affichageTexte(message, police, popup_x+225, popup_y+210, couleur, screen)
                            pygame.display.flip()

                            attendre = True
                            while attendre:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        quit()
                                    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                                        attendre = False
                        else:
                            proposition=listeAcheteur[x-1].propositionVente(coursVente)
                            if proposition!=None:
                                coursVente=proposition
                                Enchere.dernierAcheteur=listeAcheteur[x-1]
                            x-=1
                            Enchere.timerJoueur.reset()
                    elif x<=0 and Enchere.timerJoueur.tempsPassé(60):
                        tempsJoueur=5
                        Enchere.timerJoueur.reset()
                
                Blackjack.affichageTexte(str(coursVente),police,475,25,'black',screen)
                Blackjack.affichageTexte(str(Enchere.jetonsDisponibles),police,30,190,'black',screen)
                Enchere.oui.clickable=True
                Enchere.non.clickable=True

        elif jeuSelectionné=="prize":
            screen.blit(bar, (0, 0))
            Blackjack.actionBouton = Blackjack.associationBoutonVariable(Blackjack.actionBouton, boutonMenu.utilisation(screen))

            if Blackjack.actionBouton == "menu" and not boutonMenu.boutonEnfonce:
                Blackjack.actionBouton = ""
                jeuSelectionné = "menu"

            # Afficher les trophées
            succes_1.afficher(screen)
            succes_2.afficher(screen)
            succes_3.afficher(screen)
            succes_4.afficher(screen)
            succes_5.afficher(screen)
            succes_6.afficher(screen)
            succes_7.afficher(screen)
            succes_8.afficher(screen)
            
    elif lieu=="ville":
        if jeuSelectionné=="menu":
            screen.blit(ville,(0,0))
            modifierMusique(musiqueVille)
        
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonGobelets.survoler(screen))
            changementEcran(boutonGobelets,"gobelets",Goblets)

            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonBoite.survoler(screen))
            changementEcran(boutonBoite,"boite",Boite)

            # Bouton Casino
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonCasino.survoler(screen))
            if Blackjack.actionBouton=="hall" and not boutonCasino.boutonEnfonce:
                Blackjack.actionBouton=""
                lieu="hall"
            # Bouton Maison
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMaison.survoler(screen))
            if Blackjack.actionBouton=="maison" and not boutonMaison.boutonEnfonce:
                Blackjack.actionBouton=""
                lieu="maison"

        elif jeuSelectionné=="gobelets":
            screen.blit(Goblets.fond_image, (0, 0))
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
            changementEcran(boutonMenu,"menu",Goblets)
            Goblets.afficher_jetons(screen)
            if Goblets.mise==0:
                Goblets.billet_jeton5.utilisation(screen)
                Goblets.billet_jeton25.utilisation(screen)
                Goblets.billet_jeton50.utilisation(screen)
                Goblets.billet_jeton100.utilisation(screen)
            for i, pos in enumerate(Goblets.gobelets_positions):
                if not Goblets.gobelets_ouverts[i]:
                    screen.blit(Goblets.gobelet_bas_image, pos)
                else:
                    screen.blit(Goblets.gobelet_haut_image, pos)
                    if i == Goblets.bille_index:
                        bille_x = pos[0] + Goblets.gobelet_bas_image.get_width() // 2 - Goblets.bille_image.get_width() // 2
                        bille_y = pos[1] + Goblets.gobelet_bas_image.get_height() // 2  - 62
                        screen.blit(Goblets.bille_image, (bille_x, bille_y))

            if Goblets.message:
                Goblets.afficher_message(Goblets.message, -50,screen)
                Goblets.afficher_message("Cliquez sur un bouton mélanger et rejouer", -10,screen)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Goblets.animation_terminee:
                if not any(Goblets.gobelets_ouverts):
                    for i, pos in enumerate(Goblets.gobelets_positions):
                        gobelet_rect = pygame.Rect(pos[0], pos[1], Goblets.gobelet_bas_image.get_width(), Goblets.gobelet_bas_image.get_height())
                        if gobelet_rect.collidepoint(event.pos):
                            revele = True
                            Goblets.gobelets_ouverts = [True, True, True]
                            if i == Goblets.bille_index:
                                Goblets.message = "Vous avez gagné !"
                                Goblets.jetonsDisponibles += Goblets.mise * 2
                                Goblets.mise=0
                                if Goblets.cyclev>8:
                                    Goblets.cyclej=Goblets.cyclej+3
                                    Goblets.cyclev=Goblets.cyclev-7
                                if Goblets.cyclev < 8:
                                    Goblets.vitesse_max = True

                            else:
                                Goblets.message = "Vous avez perdu !"
                                Goblets.mise = 0
                                Goblets.cyclej=Goblets.cyclej-1
                                Goblets.cyclev=Goblets.cyclev+3

        elif jeuSelectionné=="boite":
            screen.blit(Boite.fond_image, (0, 0))
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonMenu.utilisation(screen))
            changementEcran(boutonMenu,"menu",Boite)
            Boite.afficher_jetons(screen)
            if Boite.mise==0:
                Boite.billet_jeton5.utilisation(screen)
                Boite.billet_jeton25.utilisation(screen)
                Boite.billet_jeton50.utilisation(screen)
                Boite.billet_jeton100.utilisation(screen)
            
            screen.blit(Boite.bouton_image, Boite.bouton_rect.topleft)
            
            if Boite.message:
                Boite.afficher_message(Boite.message, -50,screen)
            
            if Boite.timer_active:
                elapsed_time = time.time() - Boite.start_time
                remaining_time = max(0, 5 - int(elapsed_time))
                texte_timer = police.render(f"{remaining_time} sec", True, Boite.WHITE)
                screen.blit(texte_timer, (Boite.fond_largeur // 2 - 20, Boite.fond_hauteur // 2 + 60))
                
                if elapsed_time >= 5:
                    Boite.timer_active = False
                    
                    result = randint(1, 100)
                    if result <= 40:
                        Boite.jetonsDisponibles += Boite.mise * 2
                        Boite.message = "Gagné !!!!!!! Mise x2"
                    elif result <= 80:
                        Boite.jetonsDisponibles += Boite.mise // 2
                        Boite.message = "Petit gain: -50% de la mise"
                    else:
                        Boite.message = "Dommage..."
                    
                    Boite.mise = 0
                    Boite.bouton_image = pygame.transform.scale(Boite.definir_image_gobelet(), (200, 205))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if Boite.bouton_rect.collidepoint(event.pos) and not Boite.timer_active:
                        Boite.jouer()

    elif lieu=="maison":
        screen.blit(ville,(0,0))
        screen.blit(pygame.transform.scale(fondRect,(1000,600)),(0,0))
        pygame.draw.rect(screen,(255,255,255),(150, 200, 700, 200), 3)
        screen.blit(pygame.transform.scale(fondRect,(700,200)),(150,200))
        if len(Enchere.listeAchat)!=0:
            tailleX=Enchere.listeAchat[indexMaison]['tailleImg'][0]
            tailleY=Enchere.listeAchat[indexMaison]['tailleImg'][1]
            X=280-tailleX//2
            Y=300-tailleY//2
            if img==None:
                img=pygame.transform.scale(pygame.image.load(Enchere.listeAchat[indexMaison]['image']),(tailleX,tailleY))
            screen.blit(img,(X,Y))
            Blackjack.affichageTexte(f'Nom : {Enchere.listeAchat[indexMaison]["nom"]}',petitePolice,420,225,'black',screen)
            Blackjack.affichageTexte(f'Musée : {Enchere.listeAchat[indexMaison]["musée"]}',petitePolice,420,275,'black',screen)
            Blackjack.affichageTexte(f'artiste : {Enchere.listeAchat[indexMaison]["artiste"]}',petitePolice,420,325,'black',screen)
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonFlecheGauche.utilisation(screen))
            if Blackjack.actionBouton==-1 and not Bank.boutonFlecheGauche.boutonEnfonce:
                if indexMaison>0:
                    indexMaison-=1
                    img=None
                    Blackjack.actionBouton=None
            Blackjack.actionBouton=Blackjack.associationBoutonVariable(Blackjack.actionBouton,boutonFlecheDroite.utilisation(screen))
            if Blackjack.actionBouton==1 and not Bank.boutonFlecheDroite.boutonEnfonce:
                if indexMaison<len(Enchere.listeAchat)-1:
                    indexMaison+=1
                    img=None
                    Blackjack.actionBouton=None
        if boutonAnnuler.utilisation(screen)=="annuler":
            lieu="ville"
        

    # Rafraichissement de la fenêtre
    pygame.display.flip()
    clock.tick(60)
    Blackjack.timer.ajouté()
    Enchere.timerJoueur.ajouté()
# Ferme le programme
pygame.quit()