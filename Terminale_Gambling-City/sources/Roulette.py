# Roulette
# De Gabriel
import pygame
from pygame.locals import *
import random
# Toutes les notions de temps sont faites par IA car je n'ai pas su les faire fonctionner
import time,math,sources.Blackjack as Blackjack

# Image de la coque de la roulette
coque_roulette=pygame.image.load("data/texture_roulette/coque_roulette.png")

# Variables
# Les # sont fait par moi pour me repéré plus facilement
jetonsDisponibles = 0
mise = 0
paris = {} # Permettra de pouvoir enregistré les paris pour d'autres classes et sera effacé une fois fini avec pari.clear
vert = False
# Police
police = pygame.font.Font('data/fichiers_additionnels/Crang.ttf', 16)

# Classes
# Boutons
# Permet de faire donner une valeur à des boutons 
# Code utilisé de thomas(ancienne version) et j'ai retiré la petite animation de recul (à cause du lags)
class Bouton:
    def __init__(self, valeur, cheminImage, posX, posY):
        self.image = pygame.image.load(cheminImage)
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.valeur = valeur
        self.boutonEnfonce = False # Détermine si le bouton est pressé

    def utilisation(self,screen):
        """Détecte si l'utilisateur appuit sur le bouton et effectue une certaine action."""
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.boutonEnfonce:
                self.boutonEnfonce = True
                self.action()
        if pygame.mouse.get_pressed()[0] == 0 and self.boutonEnfonce:
            self.boutonEnfonce = False
        self.affichage(screen)

    def affichage(self,screen):
        """Affiche le bouton à sa position."""
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def action(self):
        pass

class Jeton(Bouton):        
    def action(self):
        """Remets les paris à zéro et augmente la mise de la valeur du jeton."""
        global mise, jetonsDisponibles, paris
        paris.clear()
        if jetonsDisponibles >= self.valeur:
            mise += self.valeur
            jetonsDisponibles -= self.valeur

class BoutonIntervalle(Bouton):
    def action(self):
        """Permet de parier sur un interval de numéro et remet à zéro les paris."""
        global paris
        paris.clear()
        paris["intervalle"] = self.valeur  # Cette ligne assigne la valeur de self.valeur à la clé "intervalle" dans le dictionnaire paris

class BoutonColonne(Bouton):
    """Attribution des valeurs aux colonnes."""
    def action(self):
        global paris
        paris.clear()
        if self.valeur == "colonne rouge":
            paris["couleur_rouge"] = self.valeur # Si self.valeur vaut "colonne_rouge", la clé "couleur_rouge" est ajoutée au dictionnaire paris, associée à self.valeur (même métode que les dictionaire).
        elif self.valeur == "colonne noire":
            paris["couleur_noire"] = self.valeur
        elif self.valeur == "colonne odd":
            paris["couleur_odd"] = self.valeur
        elif self.valeur == "colonne even":
            paris["couleur_even"] = self.valeur
        else:
            paris["colonne"] = self.valeur

class BoutonNumero(Bouton):
    """Pari sur la valeur du bouton."""
    def action(self):
        global paris
        paris.clear()
        paris["numéro"] = self.valeur 

# Roulette
# Définition de tout ce qui se retrouve indiqué avant en implémentant les colonnes et les intervales."""
class Roulette:
    def __init__(self):
        self.resultat = None
        # (utilisation  de l'IA) Les trois colonnes de la roulette sont initialisées sous forme d'ensembles (set), contenant les numéros associés à chaque colonne
        self.colonne_3 = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}
        self.colonne_2 = {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35}
        self.colonne_1 = {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34}

        # (recherche personelle en essayant d'obtenir un résulatat correspondant) fait pareil que ceux du dessus"""
        self.rouge = {2, 4, 6, 8, 10,12,14,16,18,20,22,24,26,28,30,32,34,36}
        self.even = {2, 4, 6, 8, 10,12,14,16,18,20,22,24,26,28,30,32,34,36}
        self.noir = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35}
        self.odd = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35}

    def spin(self):
        """Détermine le résultat."""
        self.resultat = random.randint(0, 36)
        # (Code grace a l'IA pour simplifier une idée de mon programe car cela était beaucoup trop long et faisais ramer le pc)
        # Cela permet de déterminer la couleur du numéro en cherchant si le numéro apartient au rouge, noire puis si n'appartient pas aux deux il devient donc vert
        couleur = "rouge" if self.resultat in self.rouge else "noir" if self.resultat in self.noir else "vert"
        return self.resultat, couleur # Stocke le résultat et sa couleur

    def verifier_gains(self):
        """Permet de vérifier les gains et de les attribuer aux intervalles pour déterminer les gains du joueur."""
        global mise, jetonsDisponibles,vert
        gains = 0
        couleur_resultat = "rouge" if self.resultat in self.rouge else "noir" if self.resultat in self.noir else "vert" # Pareil que le précédant permettant juste de vérifier
        
        # Code fait avec IA pour aider à la compréhension du fonctionnement
        if "couleur_rouge" in paris and couleur_resultat == "rouge":
            gains += mise * 2
        elif "couleur_noire" in paris and couleur_resultat == "noir":
            gains += mise * 2
        elif "couleur_even" in paris and couleur_resultat == "rouge":
            gains += mise * 2
        elif "couleur_odd" in paris and couleur_resultat == "noir":
            gains += mise * 2
        

        # Code sans IA, fait en s'inspirant des lignes au-dessus
        if "intervalle" in paris:
            if paris["intervalle"] == "1-12" and 1 <= self.resultat <= 12: # Vérifie si le numéro se trouve dans l'intervalle si la clé "intervalle" est dans 'paris'
                gains += mise * 3
            elif paris["intervalle"] == "13-24" and 13 <= self.resultat <= 24:
                gains += mise * 3
            elif paris["intervalle"] == "25-36" and 25 <= self.resultat <= 36:
                gains += mise * 3
            elif paris["intervalle"] == "1-18" and 1 <= self.resultat <= 18:
                gains += mise * 2
            elif paris["intervalle"] == "19-36" and 19 <= self.resultat <= 36:
                gains += mise * 2

        # Vérification pour chaque numéro
        if "numéro" in paris and paris["numéro"] == self.resultat:
            gains += mise * 36
            if paris["numéro"]==0:
                vert = True

        # Vérification pour chaque colonne (similaire aux intervalles)
        if "colonne" in paris:
            if paris["colonne"] == "colonne_1" and self.resultat in self.colonne_1:
                gains += mise * 3
            elif paris["colonne"] == "colonne_2" and self.resultat in self.colonne_2:
                gains += mise * 3
            elif paris["colonne"] == "colonne_3" and self.resultat in self.colonne_3:
                gains += mise * 3


        jetonsDisponibles += gains # Rend la mise + le nombre de x jetons gagnés
        mise = 0
        paris.clear()
        return gains

# La classe BoutonRoulette à été faite par moi mais une parti de mon code a dû être modifier par l'IA pour faire les animations de la balle et de la roue
class BoutonRoulette(Bouton):
    def __init__(self, valeur, cheminImage, posX, posY):
        super().__init__(valeur, cheminImage, posX, posY)
        self.resultat_texte = ""
        self.affichage_resultat_temps = 0
        self.afficher_resultat_flag = False
        self.angle = 0  
        self.tourner = False  
        self.vitesse_rotation = 1
        self.deceleration = 0.8  
        self.boule_angle = 0
        self.vitesse_boule = 14.75
        self.boule_image = pygame.image.load("data/texture_roulette/roulette_ball.png")  # Image de la boule
        self.roulette = Roulette()

    # Code réalisable graçe à la compréhention du code de l'IA précédement
    def action(self):
        """Affichage des résultats lorsque l'animation est finie."""
        resultat, couleur = roulette.spin()
        gains = roulette.verifier_gains()
        self.tourner = True
        self.angle = 0
        self.vitesse_rotation = random.randint (39, 48)
        self.vitesse_boule = random.randint (14, 16)
        self.resultat, self.couleur = roulette.spin()
        self.afficher_resultat_flag = False 
        # Toute les notions du temps ont été faites graçe à l'IA car je n'ai pas sû faire tourner cela de mon côté"""
        # Affichage des résultats (sans IA)
        if gains > 0:
            self.resultat_texte = f"Résultat: {resultat} {couleur},      Vous avez GAGNÉ !!! {gains / 2} jetons"
            self.affichage_resultat_temps = time.time()
            self.afficher_resultat_flag = True
        else:
            self.resultat_texte = f"Résultat: {resultat} {couleur},      Vous avez perdu..."
            self.affichage_resultat_temps = time.time()
            self.afficher_resultat_flag = True

    def tourner_roulette(self,screen):
        """Animation de la roulette."""
        # Code fait par IA car cela dépasse mes compétences (j'ai modifié quelques parties pour améliorer l'animation et donner de l'aléatoire)
        if self.tourner:
            self.angle += self.vitesse_rotation
            self.vitesse_rotation = max(0, self.vitesse_rotation - self.deceleration)
            if self.vitesse_rotation == 0:
                self.tourner = False
                self.afficher_resultat_flag = True
                self.affichage_resultat_temps = time.time()
            
            self.boule_angle += self.vitesse_boule
            # Réduit progressivement la distance de la boule par rapport au centre de la roulette
            boule_distance = max(0, self.vitesse_boule * 6)
            boule_x = self.rect.centerx + boule_distance * math.cos(math.radians(self.boule_angle))
            boule_y= self.rect.centery + boule_distance * math.sin(math.radians(self.boule_angle))
            # Réduit la vitesse de la boule
            self.vitesse_boule = max(0, self.vitesse_boule - 0.2)

            # Affiche la roulette en rotation
            roulette_image = pygame.transform.rotate(self.image, self.angle)
            image_rect = roulette_image.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2))
            screen.blit(roulette_image, image_rect.topleft)

            # Affiche la boule
            boule_rect = self.boule_image.get_rect(center=(boule_x, boule_y))
            screen.blit(self.boule_image, boule_rect)



    def afficher_resultat(self,screen):
        """Affiche le résultat si moins de 10 secondes se sont écoulées depuis le tirage des résultats."""
        if self.afficher_resultat_flag and (time.time() - self.affichage_resultat_temps) < 10 and self.tourner == False:
            Blackjack.affichageTexte(self.resultat_texte,police, 340, 100,'brown',screen)

        # Réinitialise le (flag) après 10 secondes
        if (time.time() - self.affichage_resultat_temps) >= 10:
            self.afficher_resultat_flag = False

# Instanciations
# Jetons
jeton1 = Jeton(1, "data/textures_blackjack/boutons/jeton_1.png", 75, 505)
jeton5 = Jeton(5, "data/textures_blackjack/boutons/jeton_5.png", 200,505)
jeton25 = Jeton(25, "data/textures_blackjack/boutons/jeton_25.png", 325,505)
jeton50 = Jeton(50, "data/textures_blackjack/boutons/jeton_50.png", 580,505)
jeton100 = Jeton(100, "data/textures_blackjack/boutons/jeton_100.png",705,505)
jeton500 = Jeton(500, "data/textures_blackjack/boutons/jeton_500.png",835,505)
jetonAllIn = Jeton(jetonsDisponibles, "data/textures_blackjack/boutons/jeton_ALLIN.png", 450,505)

# Boutons intervalles
bouton_intervalle_1_12 = BoutonIntervalle("1-12", "data/texture_roulette/roulette_special/bouton1_12.png", 476, 313)
bouton_intervalle_13_24 = BoutonIntervalle("13-24", "data/texture_roulette/roulette_special/bouton13_24.png", 580, 313)
bouton_intervalle_25_36 = BoutonIntervalle("25-36", "data/texture_roulette/roulette_special/bouton25_36.png", 684, 313)
bouton_intervalle_1_to_18 = BoutonIntervalle("1-18", "data/texture_roulette/roulette_special/bouton_intervale_1_to_18.png", 476, 343)
bouton_intervalle_19_to_36 = BoutonIntervalle("19-36", "data/texture_roulette/roulette_special/bouton_intervale_19_to_36.png", 736, 343)

# Boutons colonnes
bouton_colonne_1 = BoutonColonne("colonne_1", "data/texture_roulette/roulette_special/bouton_colonne1.png", 788, 199)
bouton_colonne_2 = BoutonColonne("colonne_2", "data/texture_roulette/roulette_special/bouton_colonne2.png", 788, 237)
bouton_colonne_3 = BoutonColonne("colonne_3", "data/texture_roulette/roulette_special/bouton_colonne3.png", 788, 275)

# Boutons couleurs et even et odd (sont identiques, c'est intentionnel)
bouton_colonne_rouge = BoutonColonne("colonne rouge", "data/texture_roulette/roulette_special/rouge.png", 580, 343)
bouton_colonne_noire = BoutonColonne("colonne noire", "data/texture_roulette/roulette_special/noire.png", 631, 343)
bouton_colonne_even = BoutonColonne("colonne enven", "data/texture_roulette/roulette_special/even.png", 528, 343)
bouton_colonne_odd = BoutonColonne("colonne odd", "data/texture_roulette/roulette_special/odd.png", 684, 343)


# Boutons numéro (je l'ai fait de cette façons car le code ne fonctionais pas en entier sur Main)
bouton_numero_0 = BoutonNumero(0, "data/texture_roulette/0-36/0.png", 450, 200)
bouton_numero_1 = BoutonNumero(1, "data/texture_roulette/0-36/1.png", 476, 200)
bouton_numero_2 = BoutonNumero(2, "data/texture_roulette/0-36/2.png", 476, 238)
bouton_numero_3 = BoutonNumero(3, "data/texture_roulette/0-36/3.png", 476, 276)
bouton_numero_4 = BoutonNumero(4, "data/texture_roulette/0-36/4.png", 502, 200)
bouton_numero_5 = BoutonNumero(5, "data/texture_roulette/0-36/5.png", 502, 238)
bouton_numero_6 = BoutonNumero(6, "data/texture_roulette/0-36/6.png", 502, 276)
bouton_numero_7 = BoutonNumero(7, "data/texture_roulette/0-36/7.png", 528, 200)
bouton_numero_8 = BoutonNumero(8, "data/texture_roulette/0-36/8.png", 528, 238)
bouton_numero_9 = BoutonNumero(9, "data/texture_roulette/0-36/9.png", 528, 276)
bouton_numero_10 = BoutonNumero(10, "data/texture_roulette/0-36/10.png", 554, 200)
bouton_numero_11 = BoutonNumero(11, "data/texture_roulette/0-36/11.png", 554, 238)
bouton_numero_12 = BoutonNumero(12, "data/texture_roulette/0-36/12.png", 554, 276)
bouton_numero_13 = BoutonNumero(13, "data/texture_roulette/0-36/13.png", 580, 200)
bouton_numero_14 = BoutonNumero(14, "data/texture_roulette/0-36/14.png", 580, 238)
bouton_numero_15 = BoutonNumero(15, "data/texture_roulette/0-36/15.png", 580, 276)
bouton_numero_16 = BoutonNumero(16, "data/texture_roulette/0-36/16.png", 606, 200)
bouton_numero_17 = BoutonNumero(17, "data/texture_roulette/0-36/17.png", 606, 238)
bouton_numero_18 = BoutonNumero(18, "data/texture_roulette/0-36/18.png", 606, 276)
bouton_numero_19 = BoutonNumero(19, "data/texture_roulette/0-36/19.png", 632, 200)
bouton_numero_20 = BoutonNumero(20, "data/texture_roulette/0-36/20.png", 632, 238)
bouton_numero_21 = BoutonNumero(21, "data/texture_roulette/0-36/21.png", 632, 276)
bouton_numero_22 = BoutonNumero(22, "data/texture_roulette/0-36/22.png", 658, 200)
bouton_numero_23 = BoutonNumero(23, "data/texture_roulette/0-36/23.png", 658, 238)
bouton_numero_24 = BoutonNumero(24, "data/texture_roulette/0-36/24.png", 658, 276)
bouton_numero_25 = BoutonNumero(25, "data/texture_roulette/0-36/25.png", 684, 200)
bouton_numero_26 = BoutonNumero(26, "data/texture_roulette/0-36/26.png", 684, 238)
bouton_numero_27 = BoutonNumero(27, "data/texture_roulette/0-36/27.png", 684, 276)
bouton_numero_28 = BoutonNumero(28, "data/texture_roulette/0-36/28.png", 710, 200)
bouton_numero_29 = BoutonNumero(29, "data/texture_roulette/0-36/29.png", 710, 238)
bouton_numero_30 = BoutonNumero(30, "data/texture_roulette/0-36/30.png", 710, 276)
bouton_numero_31 = BoutonNumero(31, "data/texture_roulette/0-36/31.png", 736, 200)
bouton_numero_32 = BoutonNumero(32, "data/texture_roulette/0-36/32.png", 736, 238)
bouton_numero_33 = BoutonNumero(33, "data/texture_roulette/0-36/33.png", 736, 276)
bouton_numero_34 = BoutonNumero(34, "data/texture_roulette/0-36/34.png", 762, 200)
bouton_numero_35 = BoutonNumero(35, "data/texture_roulette/0-36/35.png", 762, 238)
bouton_numero_36 = BoutonNumero(36, "data/texture_roulette/0-36/36.png", 762, 276)

# Roulette
roulette = Roulette()
boutonRoulette = BoutonRoulette(None, "data/texture_roulette/roulette.png", 100, 225)