# Machine à sous
# De Raphaël
import pygame
import random

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Gambling city")
clock = pygame.time.Clock()
running = True

# code copier de Blackjack.py
police=pygame.font.Font('data/fichiers_additionnels/Crang.ttf',16)
def affichageTexte(texte,font,posX,posY,color):
    imageTexte=font.render(texte,True,color)
    screen.blit(imageTexte,(posX,posY))

jetonsDisponibles = 500
mise = 0
 # test zoom d'image tuto : https://www.tutorialspoint.com/how-to-rotate-and-scale-images-using-pygame
 # avec explication de chatGPT car le programme ne fonctionnait pas
class Bouton :
    def __init__(self,chemin,scale,position_x,position_y):
        self.spin=pygame.image.load(chemin)
        self.spin_test = pygame.transform.scale(self.spin, (self.spin.get_width() * scale, self.spin.get_height() * scale))
        self.x = position_x
        self.y = position_y
        self.spin_test_rect = self.spin_test.get_rect(topleft=(self.x, self.y))
        self.clicked = False
        self.jackpot = False

    def affichage(self):
        """Affiche le bouton à sa position."""
        screen.blit(self.spin_test,self.spin_test_rect)

    def clic(self,events):
        """Vérifie dans les events pygame si le bouton de la souris est pressé.
        Si c'est le cas on fait tourner la machine."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.spin_test_rect.collidepoint(mouse_pos) and mise > 0 :
                    self.clicked = True
                    self.spin_test_rect.move_ip(2,2)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.clicked == True :
                    self.clicked = False
                    self.spin_test_rect.move_ip(-2,-2)
                    self.gauche, self.milieu, self.droite = random.choices(fruit, weights=proba_fruit, k=3)
                    gauche_bis = fruit.index(self.gauche)
                    milieu_bis = fruit.index(self.milieu)
                    droite_bis = fruit.index(self.droite)
                    roue1.changeFruit(doc_fruit[gauche_bis])
                    roue2.changeFruit(doc_fruit[milieu_bis])
                    roue3.changeFruit(doc_fruit[droite_bis])
                    self.calcul()

    def calcul(self):
        """Calcul des gains."""
        global mise, jetonsDisponibles
        if self.gauche == self.milieu == self.droite:
            if self.gauche == "carote" :
                jetonsDisponibles+=100*mise
            if self.gauche == "coco" :
                jetonsDisponibles+=7*mise
            if self.gauche == "orange" :
                jetonsDisponibles+=4*mise
            if self.gauche == "pastèque" :
                jetonsDisponibles+=50*mise
            if self.gauche == "pomme" :
                jetonsDisponibles+=17*mise
        if self.gauche == "coin" or self.milieu == "coin" or self.droite == "coin":
            jetonsDisponibles+=1000+mise
            self.jackpot = True
        mise=0

class Trophe:
    def __init__(self,chemin,scale,position_x,position_y):
        self.trophe=pygame.image.load(chemin)
        self.trophe_sise = pygame.transform.scale(self.trophe, (self.trophe.get_width() * scale, self.trophe.get_height() * scale))
        self.x = position_x   
        self.y = position_y
        self.trophe_sise_rect = self.trophe_sise.get_rect(topleft=(self.x, self.y))

    def afficher(self):
        """Affiche le trophé à sa position."""
        screen.blit(self.trophe_sise,self.trophe_sise_rect)

class Jeton :
    def __init__(self,valeur,chemin,scale,position_x,position_y):
        self.jeton=pygame.image.load(chemin)
        self.jeton_sise = pygame.transform.scale(self.jeton, (self.jeton.get_width() * scale, self.jeton.get_height() * scale))
        self.x = position_x
        self.y = position_y
        self.jeton_sise_rect = self.jeton_sise.get_rect(topleft=(self.x, self.y))
        self.valeur = valeur
        self.clicked = False

    def affichage(self):
        """Affichage du jeton à sa position."""
        screen.blit(self.jeton_sise,self.jeton_sise_rect)

    def clic(self,events):
        """Vérifie dans les events pygame si le bouton de la souris est pressé.
        Si c'est le cas ajoute sa valeur à la mise et la retire des ketons disponibles."""
        global mise, jetonsDisponibles
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.jeton_sise_rect.collidepoint(mouse_pos):
                    self.clicked = True
                    self.jeton_sise_rect.move_ip(2,2)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.clicked == True :
                    self.clicked = False
                    self.jeton_sise_rect.move_ip(-2,-2)
                    if jetonsDisponibles >= self.valeur :
                        mise+=self.valeur
                        jetonsDisponibles-=self.valeur

    def utilisation(self,events):
        """Utilisation du bouton (affichage et action)"""
        self.affichage()
        self.clic(events)

class Roue:
    def __init__(self,chemin,scale,position_x,position_y):
        self.fruit=pygame.image.load(chemin)
        self.scale=scale
        self.fruit_sise = pygame.transform.scale(self.fruit, (self.fruit.get_width() * self.scale, self.fruit.get_height() * self.scale))
        self.x = position_x
        self.y = position_y
        self.fruit_sise_rect = self.fruit_sise.get_rect(topleft=(self.x, self.y))

    def changeFruit(self,chemin):
        """Change le fruit."""
        self.fruit=pygame.image.load(chemin)
        self.fruit_sise = pygame.transform.scale(self.fruit, (self.fruit.get_width() * self.scale, self.fruit.get_height() * self.scale))

    def affichage(self):
        """Affiche le fruit."""
        screen.blit(self.fruit_sise,(self.x,self.y))
    
# Liste des fruits, de leurs images et de leurs proba
fruit = ["carote","coco","orange","pastèque","pomme","coin"]
doc_fruit = ["data/textures_machine_à_sous/Fruits/carote.png",
             "data/textures_machine_à_sous/Fruits/coco.png",
             "data/textures_machine_à_sous/Fruits/orange.png",
             "data/textures_machine_à_sous/Fruits/pastèque.png",
             "data/textures_machine_à_sous/Fruits/pomme.png",
             "data/textures_machine_à_sous/Fruits/coin.png"]
proba_fruit = [0.05, 0.25, 0.5, 0.1, 0.199, 0.001]
#[0.05, 0.25, 0.5, 0.1, 0.199, 0.001] ( au cas ou je doit faire des test)

# Instanciations
# Bouton spin
spin = Bouton ("data/textures_machine_à_sous/bouton_tourner_roue.png",3,405,350)
# Jetons
jeton1 = Jeton(1,"data/textures_blackjack/boutons/jeton_1.png", 1, 75, 505)
jeton5 = Jeton (5,"data/textures_blackjack/boutons/jeton_5.png", 1, 200, 505)
jeton25 = Jeton (25,"data/textures_blackjack/boutons/jeton_25.png", 1, 325, 505)
jeton50 = Jeton (50,"data/textures_blackjack/boutons/jeton_50.png", 1, 580, 505)
jeton100 = Jeton (100,"data/textures_blackjack/boutons/jeton_100.png", 1, 705, 505)
jeton500 = Jeton (500,"data/textures_blackjack/boutons/jeton_500.png", 1, 835, 505)
jetonAllIn = Jeton (jetonsDisponibles,"data/textures_blackjack/boutons/jeton_ALLIN.png", 1, 458, 505)
# Roue de la machine
roue1 = Roue("data/textures_machine_à_sous/Fruits/coin.png",4,235,200)
roue2 = Roue("data/textures_machine_à_sous/Fruits/coin.png",4,440,200)
roue3 = Roue("data/textures_machine_à_sous/Fruits/coin.png",4,645,200)
# Trophé secret
win = Trophe("data/textures_machine_à_sous/trophe.png",4,840,252)