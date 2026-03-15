import pygame
from pygame.locals import *
from random import *
import sources.Blackjack as Blackjack

# Variables
listeCarte=[]
actionBouton=""
mise=0
jetonsDisponibles=0
pari=""
egaliter = False

commencerPartie=False
# Classes
class JeuCarte:
    def __init__(self,statut,posX,posY):
        self.statut=statut
        self.valeurJeu=0
        self.posX=posX
        self.posY=posY
        self.verifier=False
        self.jeu=[]
    
    def composition(self):
        for i in range(2):
            self.ajout()

    def ajout(self):
        self.jeu.append(listeCarte.pop())

    def affichage(self,screen):
        x=self.posX
        for i in range(len(self.jeu)):
            screen.blit(self.jeu[i][0].image,(x,self.posY))
            if i<1:
                if self.statut=="player":
                    x-=65
                else:
                    x+=65
            else:
                if self.statut=="player":
                    x-=85
                else:
                    x+=85
    
    def calculValeur(self):
        valeur=0
        for carte in self.jeu:
            if carte[1]=="as":
                valeur+=1
            elif carte[1] in ["roi","reine","valet","10"]:
                valeur+=0
            else:
                valeur+=int(carte[1])
        if valeur>=10:
            valeur-=10*(valeur//10)
        self.valeurJeu=valeur

class ZonePari:
    def __init__(self,posX,posY,long,haut,img,type):
        self.image=pygame.image.load(img)
        self.rect=Rect(posX,posY,long,haut)  
        self.coordonnées=(posX,posY)  
        self.type=type
        self.estParié=False

    def utilisation(self,autresZone,screen,décalage=0):
        mousePos=pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]==1 and not self.estParié:
                for elt in autresZone:
                    if elt.estParié:
                        elt.estParié=False
                self.estParié=True
        self.affichage(screen,décalage)

    def affichage(self,screen,décalage=0):
        if self.estParié:
            screen.blit(self.image,(self.coordonnées[0]+décalage,self.coordonnées[1]))
    
# Fonctions
def partie(screen):
    global commencerPartie,actionBouton,pari,jetonsDisponibles,mise
    # Définition du pari du joueur
    for zone in listeZone:
        if zone.estParié:
            pari=zone.type
    pariJoueur.utilisation(listeZone,screen)
    pariEquality.utilisation(listeZone,screen,15)
    pariBank.utilisation(listeZone,screen)
    # Prends la mise du joueur via les jetons
    for jeton in listeJetons:
        coupleJetonsMise=jeton.utilisation(screen,jetonsDisponibles,mise)
        if coupleJetonsMise!=None:
            if coupleJetonsMise[1]!=0:
                jetonsDisponibles=coupleJetonsMise[0]
                mise=coupleJetonsMise[1]
        jetonAllIn.valeur=jetonsDisponibles

    jeuJoueur.verifier=False    # Définie la vérification des jeux sur False
    jeuBank.verifier=False
    actionBouton=Blackjack.associationBoutonVariable(actionBouton,boutonStart.utilisation(screen))
    if actionBouton=="commencer" and mise!=0 and pari!="":
        jeuJoueur.composition()
        jeuBank.composition()
        commencerPartie=True
    else:
        actionBouton=""

def finPartie(jeuJoueur,jeuCasino,screen):
    global actionBouton,commencerPartie
    Blackjack.timer.bloquerValeur()
    jeuBank.calculValeur()
    jeuJoueur.calculValeur()
    for jeton in listeJetons:
        jeton.affichage_sombre(screen)
    boutonStart.affichage_sombre(screen)
    pariJoueur.affichage(screen)
    pariEquality.affichage(screen,15)
    pariBank.affichage(screen)
    # Vérification du jeu du joueur
    if len(jeuJoueur.jeu)<3 and jeuJoueur.valeurJeu<6 and not jeuJoueur.verifier:
        if Blackjack.timer.tempsPassé(60):
            jeuJoueur.ajout()
            jeuJoueur.verifier=True
            Blackjack.timer.augmenterValeurBloquée(60)
    else:
        jeuJoueur.verifier=True
    # Vérification du jeu de la banque
    if len(jeuCasino.jeu)<3 and not jeuCasino.verifier:
        if Blackjack.timer.tempsPassé(60):
            if jeuCasino.valeurJeu==6 and jeuJoueur.valeurJeu in [6,7]:
                jeuCasino.ajout()
            elif jeuCasino.valeurJeu==5 and jeuJoueur.valeurJeu in [4,5,6,7]:
                jeuCasino.ajout()
            elif jeuCasino.valeurJeu==4 and jeuJoueur.valeurJeu in [2,3,4,5,6,7]:
                jeuCasino.ajout()
            elif jeuCasino.valeurJeu==3 and not jeuJoueur.valeurJeu==8:
                jeuCasino.ajout()
            elif jeuCasino.valeurJeu<3:
                jeuCasino.ajout()
            jeuCasino.verifier=True
            Blackjack.timer.augmenterValeurBloquée(60)
    else:
        jeuCasino.verifier=True
    # Attribution de la victoire et de la mise
    if jeuCasino.verifier and jeuJoueur.verifier and Blackjack.timer.tempsPassé(60):
        vainqueur(jeuCasino,jeuJoueur)
        Blackjack.recuperationCartes(jeuJoueur,listeCarte)
        Blackjack.recuperationCartes(jeuCasino,listeCarte)
        actionBouton=""
        commencerPartie=False
        Blackjack.timer.reset()

def vainqueur(jeuCasino,jeuJoueur):
    global jetonsDisponibles,mise,egaliter
    if pari=="joueur" and jeuJoueur.valeurJeu>jeuCasino.valeurJeu:
        jetonsDisponibles+=mise*2
        mise=0
    elif pari=="bank" and jeuCasino.valeurJeu>jeuJoueur.valeurJeu:
        jetonsDisponibles+=int(mise*1.95)
        mise=0
    elif pari=="equality" and jeuJoueur.valeurJeu==jeuCasino.valeurJeu:
        jetonsDisponibles+=mise*8
        mise=0
        egaliter = True
    else:
        mise=0

# Instanciations
jeuJoueur=JeuCarte("player",302,201)
jeuBank=JeuCarte("bank",648,201)

boutonStart=Blackjack.Bouton("commencer","data/boutonCommencer.png",450,371,"data/bouton_sombre/boutonCommencer_sombre.png")

pariJoueur=ZonePari(200,425,188,67,"data/pion.png","joueur")
pariEquality=ZonePari(391,425,217,67,"data/pion.png","equality")
pariBank=ZonePari(611,425,188,67,"data/pion.png","bank")
listeZone=[pariJoueur,pariEquality,pariBank]

jeton1=Blackjack.Bouton(1,"data/textures_blackjack/boutons/jeton_1.png",75,505,"data/bouton_sombre/jeton_1_sombre.png","jeton")
jeton5=Blackjack.Bouton(5,"data/textures_blackjack/boutons/jeton_5.png",200,505,"data/bouton_sombre/jeton_5_sombre.png","jeton")
jeton25=Blackjack.Bouton(25,"data/textures_blackjack/boutons/jeton_25.png",325,505,"data/bouton_sombre/jeton_25_sombre.png","jeton")
jeton50=Blackjack.Bouton(50,"data/textures_blackjack/boutons/jeton_50.png",580,505,"data/bouton_sombre/jeton_50_sombre.png","jeton")
jeton100=Blackjack.Bouton(100,"data/textures_blackjack/boutons/jeton_100.png",705,505,"data/bouton_sombre/jeton_100_sombre.png","jeton")
jeton500=Blackjack.Bouton(500,"data/textures_blackjack/boutons/jeton_500.png",835,505,"data/bouton_sombre/jeton_500_sombre.png","jeton")
jetonAllIn=Blackjack.Bouton(jetonsDisponibles,"data/textures_blackjack/boutons/jeton_ALLIN.png",450,505,"data/bouton_sombre/jeton_allin_sombre.png","jeton")
listeJetons=[jeton1,jeton5,jeton25,jeton50,jeton100,jeton500,jetonAllIn]