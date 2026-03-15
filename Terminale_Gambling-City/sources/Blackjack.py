# Blackjack (de Thomas SOIDEZ)
import pygame
from pygame.locals import *
from random import *

# Variables
pygame.init()
listesCartes=[]
actionBouton=""
commencerPartie=False
afficherResultat=False
blackjack = False
jetonsDisponibles=0
mise=0

# Classes
# Création de la classe Bouton (tutoriel utilisé pour la création du bouton : https://youtu.be/G8MYGDf_9ho)
class Bouton:
    def __init__(self,valeur,cheminImage,posX,posY,img_sombre=None,type="bouton",police=None):
        if type=="texte":
            self.image=police.render(cheminImage,True,'White')
        else:
            self.image=pygame.image.load(cheminImage)
        if img_sombre!=None:
            self.image_sombre=pygame.image.load(img_sombre)
        else:
            self.image_sombre=None
        self.rect=self.image.get_rect()
        self.rect.topleft=(posX,posY)   
        self.coorDefaut=(posX,posY)     
        self.valeur=valeur
        self.categorie=type
        self.boutonEnfonce=False # Variable booléénne afin de savoir si le jeton est pressé ou non
        self.clickable=True

    def utilisation(self,screen,jetons=None,mise=None):
        """Permet de détecter si l'utilisateur appuit sur le bouton.
        Si le bouton est pressé, il fait une petite animation et execute une action donnée."""
        self.affichage(screen,jetons)
        mousePos=pygame.mouse.get_pos() # Détecte la position de la souris
        if self.rect.collidepoint(mousePos): # Détecte si la souris est sur la surface bouton
            if self.categorie=="texte":
                pygame.draw.line(screen, 'white', (self.coorDefaut[0], self.coorDefaut[1] + 30), (self.rect.topright[0], self.coorDefaut[1] + 30), 2)
            if pygame.mouse.get_pressed()[0]==1 and self.boutonEnfonce==False: # Détecte si le bouton gauche de la souris est pressé
                self.boutonEnfonce=True
                self.rect.x+=2
                self.rect.y+=2
                return self.action(jetons,mise)
        if pygame.mouse.get_pressed()[0]==0 and self.boutonEnfonce==True:
            self.boutonEnfonce=False
            self.rect.topleft=self.coorDefaut

    def affichage(self,screen,jetons=None):
        """Affiche le bouton sur l'écran à une position donnée."""
        if self.categorie!="jeton":
            screen.blit(self.image,(self.rect.x, self.rect.y))
        else:
            if jetons>=self.valeur and jetons>0:
                screen.blit(self.image,(self.rect.x, self.rect.y))
            else:
                self.affichage_sombre(screen)

    def affichage_sombre(self,screen):
        """Affiche le bouton sur l'écran à une position donnée (sert à signaler à l'utilisateur que le bouton n'est pas activable)."""
        screen.blit(self.image_sombre,(self.coorDefaut[0], self.coorDefaut[1]))

    def action(self,jetons,mise): 
        """Modifie la variable actionBouton avec la valeur du bouton ou ajoute à la mise la valeur du bouton et retire cette valeur aux jetons disponibles de l'utilisateur."""
        if self.categorie=="jeton":
            if jetons>=self.valeur:
                mise+=self.valeur
                jetons-=self.valeur
            return (jetons,mise)
        else:    
            return self.valeur

# Création de la classe Carte
class Carte:
    def __init__(self,symbole,valeur,img):
        self.symbole=symbole
        self.valeur=valeur
        self.image=pygame.image.load(img)
        self.rect=self.image.get_rect()
        self.imageCachee=pygame.image.load("data/textures_blackjack/cartes/carte_cachee.png")

# Création de la classe JeuCarte
class JeuCarte:
    def __init__(self,posX,posY,croupier):
        self.valeurTot=0
        self.posX=posX
        self.posY=posY
        self.jeu=[]
        self.croupier=croupier

    def constitution(self):
        """Ajoute les 2 premières cartes au jeu du joueur."""
        for i in range(2):
            self.piocher()

    def piocher(self):
        """Ajoute 1 carte au jeu du joueur si la valeur de son jeu n'excède pas 21."""
        if self.valeurTot<21:
            self.jeu.append(listesCartes.pop())

    def valeurJeu(self):
        """Permet de calculer la valeur totale des cartes dans le jeu du joueur et de l'afficher à une position donnée.
        Spécificités :  - Figures = 10
                        - As = 11 ou 1 (si arrange le joueur)"""
        valeurCalculé=0
        nbAs=0
        nbAs11Comptabilisé=0
        for carte in self.jeu:
            if carte[1]=='as':
                nbAs+=1
            elif carte[1] in ['valet','reine','roi']:
                valeurCalculé+=10
            else:
                valeurCalculé+=int(carte[1])
        while nbAs>0:
            if valeurCalculé+11>21:
                valeurCalculé+=1
                nbAs-=1
            elif valeurCalculé+11<=21:
                valeurCalculé+=11
                nbAs11Comptabilisé+=1
                nbAs-=1
        if valeurCalculé>21 and nbAs11Comptabilisé>0:
            while valeurCalculé>21 or nbAs11Comptabilisé>0:
                valeurCalculé-=10
                nbAs11Comptabilisé-=1
        self.valeurTot=valeurCalculé
        
    def affichageJeu(self,screen):
        """Affiche les cartes du joueur les unes à côté des autres.
        Seul la 1ère carte du croupier n'est afficher jusqu'au comptage des points."""
        x=self.posX
        if self.croupier and actionBouton!="rester":
            for carte in self.jeu:
                if carte==self.jeu[0]:
                    screen.blit(carte[0].image,(x,self.posY))
                    x-=45
                else:
                    screen.blit(carte[0].imageCachee,(x,self.posY))
                    x-=45
        else:    
            for carte in self.jeu:
                screen.blit(carte[0].image,(x,self.posY))
                x-=45

# Création de la classe Timer
class Timer:
    def __init__(self):
        self.valeur=0
        self.sauvegardé=False
        self.valeurBloqué=0
    
    def ajouté(self):
        """Ajoute 1 au timer à la fin de la boucle."""
        self.valeur+=1

    def reset(self):
        """Remet le timer à 0."""
        self.valeur=0
        self.sauvegardé=False
        self.valeurBloqué=0

    def bloquerValeur(self):
        """Garde en mémoire une valeur."""
        if self.sauvegardé==False:
            self.valeurBloqué=self.valeur
            self.sauvegardé=True

    def augmenterValeurBloquée(self,nb):
        """Augmenter la valeur sauvegardée d'un certain nombre."""
        self.valeurBloqué+=nb
    
    def tempsPassé(self,temps):
        """Compare si un laps de temps donné est passé entre le timer et la valeur bloquée."""
        return self.valeurBloqué==self.valeur-temps


# Fonctions
# Fonction constituant la pioche
def constitutionPioche(liste):
    """Ajoute dans une liste les 52 cartes et les mélanges."""
    for symb in ["trefle","pique","carreau","coeur"]:
        for val in ["as","2","3","4","5","6","7","8","9","10","valet","reine","roi"]:
            carte=Carte(symb,val,f"data/textures_blackjack/cartes/{symb}/{val}_{symb}.png")
            liste.append((carte,val))
    shuffle(liste)

# Fonction récupérant les cartes des joueurs et les remets dans la pioche
def recuperationCartes(jeu,liste):
    """Remet dans la pioche les cartes des joueurs."""
    for carte in range(len(jeu.jeu)):
        liste.append(jeu.jeu.pop())
    shuffle(liste)

# Fonction comparant la valeur des jeux
def calculResultat(jeu1,jeu2):
    """Détermine le gagnant parmi les 2 joueurs."""
    global jetonsDisponibles,mise,blackjack
    if jeu1.valeurTot==21 and len(jeu1.jeu)==2 and jeu1.valeurTot!=jeu2.valeurTot:
        jetonsDisponibles+=int(mise*2.5)
        mise=0
        blackjack = True
    else:
        if jeu1.valeurTot==jeu2.valeurTot and jeu1.valeurTot<=21:
            jetonsDisponibles+=mise
            mise=0
        elif jeu1.valeurTot<jeu2.valeurTot and jeu2.valeurTot<=21 or jeu1.valeurTot>21:
            mise=0
        elif jeu1.valeurTot>jeu2.valeurTot and jeu1.valeurTot<=21 or jeu2.valeurTot>21:
            jetonsDisponibles+=mise*2
            mise=0

# Affichage du texte (tutoriel utilisé : http://www.codingwithruss.com/pygame/working-with-text-in-pygame/)
def affichageTexte(texte,font,posX,posY,color,screen):
    """Affiche un certain texte dans une certaine couleur à un emplacement donné."""
    imageTexte=font.render(texte,True,color)
    screen.blit(imageTexte,(posX,posY))

# Déroulement de la partie
def preparation(screen,listeJetons):
    """Permet au joueur de miser ses jetons puis une fois qu'il confirme sa mise les jeux sont constitué."""
    global commencerPartie,actionBouton,jetonsDisponibles,mise
    # Affichage des jetons et éxecution
    for jeton in listeJetons:
        coupleJetonsMise=jeton.utilisation(screen,jetonsDisponibles,mise)
        if coupleJetonsMise!=None:
            if coupleJetonsMise[1]!=0:
                jetonsDisponibles=coupleJetonsMise[0]
                mise=coupleJetonsMise[1]
        jetonAllIn.valeur=jetonsDisponibles # La valeur du jeton All In étant une variable doit être rafraichit après avoir subi une modification dans la boucle

    boutonDoubler.affichage_sombre(screen)
    boutonPioche.affichage_sombre(screen)
    boutonRester.affichage_sombre(screen)

    actionBouton=associationBoutonVariable(actionBouton,boutonMiser.utilisation(screen))
    if actionBouton=="miser" and mise>0:
        commencerPartie=True
        monJeu.constitution()
        jeuAdverse.constitution()
        actionBouton=""
        timer.reset()
    elif actionBouton=="miser" and mise==0:
        actionBouton=""

def tourJoueur(screen,fond,police):
    """Permet au joueur de piocher une carte, doubler sa mise et de confirmer son jeu."""
    global jetonsDisponibles,mise,actionBouton
    # Affichage des jetons sombres
    for jeton in listeJetons:
        jeton.affichage_sombre(screen)
    boutonMiser.affichage_sombre(screen)
    if actionBouton=="rester": 
        finDePartie(screen,fond,police)
    else:
        # Affichage du bouton de pioche et exécution
        actionBouton=associationBoutonVariable(actionBouton,boutonPioche.utilisation(screen))
        if actionBouton=="piocher":
            monJeu.piocher()
            actionBouton=""
        # Affichage du bouton "Doubler" et exécution
        if len(monJeu.jeu)==2 and jetonsDisponibles-mise>=0:
            actionBouton=associationBoutonVariable(actionBouton,boutonDoubler.utilisation(screen))
            if actionBouton=="doubler":
                monJeu.piocher()
                jetonsDisponibles-=mise
                mise+=mise
                actionBouton="rester"
        else:
            boutonDoubler.affichage_sombre(screen)

        if monJeu.valeurTot>21:
            actionBouton="rester"
        # Affichage du bouton "Rester" et fin de partie
        actionBouton=associationBoutonVariable(actionBouton,boutonRester.utilisation(screen))

def finDePartie(screen,fond,police):
    """Affiche le jeu adverse, lui permet de piocher jusqu'à ce qu'il excède ou vaut la valeur 17, définit le gagnant puis revient au départ."""
    global commencerPartie,actionBouton
    timer.bloquerValeur()
    boutonDoubler.affichage_sombre(screen)
    boutonPioche.affichage_sombre(screen)
    boutonRester.affichage_sombre(screen)
    affichageTexte(f"Valeur du jeu : {jeuAdverse.valeurTot}",police,415,250,'white',screen)
    if jeuAdverse.valeurTot<17 and timer.tempsPassé(60) and monJeu.valeurTot>=jeuAdverse.valeurTot and monJeu.valeurTot<=21:
        jeuAdverse.piocher()
        timer.augmenterValeurBloquée(60)
    elif jeuAdverse.valeurTot>=17 and timer.tempsPassé(60) or monJeu.valeurTot<jeuAdverse.valeurTot and timer.tempsPassé(60) or monJeu.valeurTot>21 and timer.tempsPassé(60):
        calculResultat(monJeu,jeuAdverse)
        recuperationCartes(monJeu,listesCartes)
        recuperationCartes(jeuAdverse,listesCartes)
        screen.blit(fond,(0,0))
        commencerPartie=False
        actionBouton=""
        timer.reset()

def affichages(screen,police):
    """Affiche les jetons du joueur ainsi que sa mise."""
    # Affichage des variables
    affichageTexte(str(jetonsDisponibles),police,145,45,'brown',screen)
    affichageTexte(str(mise),police,825,45,'brown',screen)
    
    # Affichage du jeu de cartes de l'utilisateur
    monJeu.affichageJeu(screen)
    monJeu.valeurJeu()
    affichageTexte(f"Valeur du jeu : {monJeu.valeurTot}",police,415,450,'white',screen)

    jeuAdverse.affichageJeu(screen)
    jeuAdverse.valeurJeu()

def associationBoutonVariable(variable,action):
    x=action
    if x!=None:
        return x
    else:
        return variable
    
# Instanciations
# Instanciation des jetons
jeton1=Bouton(1,"data/textures_blackjack/boutons/jeton_1.png",75,505,"data/bouton_sombre/jeton_1_sombre.png","jeton")
jeton5=Bouton(5,"data/textures_blackjack/boutons/jeton_5.png",200,505,"data/bouton_sombre/jeton_5_sombre.png","jeton")
jeton25=Bouton(25,"data/textures_blackjack/boutons/jeton_25.png",325,505,"data/bouton_sombre/jeton_25_sombre.png","jeton")
jeton50=Bouton(50,"data/textures_blackjack/boutons/jeton_50.png",580,505,"data/bouton_sombre/jeton_50_sombre.png","jeton")
jeton100=Bouton(100,"data/textures_blackjack/boutons/jeton_100.png",705,505,"data/bouton_sombre/jeton_100_sombre.png","jeton")
jeton500=Bouton(500,"data/textures_blackjack/boutons/jeton_500.png",835,505,"data/bouton_sombre/jeton_500_sombre.png","jeton")
jetonAllIn=Bouton(jetonsDisponibles,"data/textures_blackjack/boutons/jeton_ALLIN.png",450,505,"data/bouton_sombre/jeton_allin_sombre.png","jeton")
listeJetons=[jeton1,jeton5,jeton25,jeton50,jeton100,jeton500,jetonAllIn]

# Instanciation des boutons
boutonPioche=Bouton("piocher","data/textures_blackjack/boutons/piocher.png",754,399,"data/bouton_sombre/piocher_sombre.png")
boutonRester=Bouton("rester","data/textures_blackjack/boutons/rester.png",649,399,"data/bouton_sombre/rester_sombre.png")
boutonMiser=Bouton("miser","data/textures_blackjack/boutons/miser.png",649,344,"data/bouton_sombre/miser_sombre.png")
boutonDoubler=Bouton("doubler","data/textures_blackjack/boutons/doubler.png",754,344,"data/bouton_sombre/doubler_sombre.png")

# Instanciation des jeux de cartes
monJeu=JeuCarte(474,366,False)
jeuAdverse=JeuCarte(474,145,True)
timer=Timer()