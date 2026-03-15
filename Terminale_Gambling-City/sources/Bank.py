import pygame
from pygame.locals import *
import sources.Blackjack as Blackjack

jetonsDisponibles=0
dette=0
endetté=False
action=None

indexVente=0
venteConclu=False

bulle=pygame.image.load("data/textures_bank/bulleGameOver.png")

# Fonctions
def emprunt(bouton):
    """Ajoute à la bourse de jetons de l'utilisateur la valeur du bouton et augmente sa dette du même nombre."""
    global jetonsDisponibles,dette
    if Blackjack.actionBouton==bouton:
        Blackjack.timer.bloquerValeur()
        if Blackjack.timer.tempsPassé(20):
            jetonsDisponibles+=bouton
            dette+=bouton
            Blackjack.actionBouton=""
            Blackjack.timer.reset()

def remboursement(bouton):
    """Si le joueur est en possession du nombre suffisant de jetons, il peut rembourser sa dette."""
    global jetonsDisponibles,dette
    if Blackjack.actionBouton==dette:
        Blackjack.timer.bloquerValeur()
        if Blackjack.timer.tempsPassé(20):
            jetonsDisponibles-=bouton
            dette=0
            Blackjack.actionBouton=""
            Blackjack.timer.reset()

def expulsion(screen,running,sauvegarde):
    """Ferme le jeu si la dette de l'utilisateur excède 2000 jetons."""
    global endetté
    if dette>2000:
        endetté=True
        sauvegarde.reset()
        Blackjack.timer.bloquerValeur()
        screen.blit(bulle,(550,25))
        if Blackjack.timer.tempsPassé(240):
            running=False
    return running

# Instanciation des boutons
boutonEmprunt100=Blackjack.Bouton(100,"data/textures_bank/emprunt100.png",49,524,)
boutonEmprunt500=Blackjack.Bouton(500,"data/textures_bank/emprunt500.png",749,524,)
boutonRembourser=Blackjack.Bouton(dette,"data/textures_bank/rembourser.png",49,524,"data/bouton_sombre/rembourser_sombre.png")
boutonEmprunter=Blackjack.Bouton("emprunt","data/textures_bank/emprunter.png",399,524,"data/bouton_sombre/emprunter_sombre.png")
boutonVendreOeuvre=Blackjack.Bouton("vendreOeuvre","data/textures_bank/vendre_oeuvre.png",749,524)
boutonVendre=Blackjack.Bouton("vendre","data/textures_bank/vendre.png",749,524)

boutonFlecheGauche=Blackjack.Bouton(-1,"data/textures_bank/fleche_gauche.png",49,524)
boutonAnnuler=Blackjack.Bouton("annuler","data/textures_bank/annuler.png",49+boutonFlecheGauche.image.get_width(),524)
boutonFlecheDroite=Blackjack.Bouton(1,"data/textures_bank/fleche_droite.png",49+boutonFlecheGauche.image.get_width()+boutonAnnuler.image.get_width(),524)