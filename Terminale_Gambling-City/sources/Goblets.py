import pygame
import random

pygame.init()

fond_image = pygame.image.load("data/texture_gobelet/plateaux_jeux_gobelet.png")
fond_image = pygame.transform.scale(fond_image, (1000, 600))

fond_largeur = fond_image.get_width()
fond_hauteur = fond_image.get_height()

WHITE = (255, 255, 255)

bille_image = pygame.transform.scale(
    pygame.image.load("data/texture_gobelet/gobelet_ball.png"), (200, 200)
)
gobelet_bas_image = pygame.transform.scale(
    pygame.image.load("data/texture_gobelet/gobelet_bas.png"), (60, 75)
)
gobelet_haut_image = pygame.transform.scale(
    pygame.image.load("data/texture_gobelet/gobelet_haut.png"), (60, 75)
)

bouton_image = pygame.image.load("data/textures_blackjack/boutons/doubler.png")
police = pygame.font.Font('data/fichiers_additionnels/Crang.ttf', 16)

gobelets_positions = [
    (320,180),  # Premier gobelet à gauche
    (470, 180), # Gobelet du milieu
    (620,180)  # Gobelet à droite
]

# Variables du jeu
jetonsDisponibles = 1000
mise = 0
paris = {}
bille_index = random.randint(0, 2)
revele = True
gobelets_ouverts = [True, True, True]
message = ""
animation_terminee = False
vitesse_max = False

class Bouton:
    def __init__(self, valeur, cheminImage, posX, posY):
        self.image = pygame.transform.scale(pygame.image.load(cheminImage), (75, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.valeur = valeur
        self.boutonEnfonce = False

    def utilisation(self,screen):
        """Détecte si l'utilisateur appuit sur le bouton et effectue une certaine action."""
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.boutonEnfonce:
                self.boutonEnfonce = True
                self.action(screen)
        if pygame.mouse.get_pressed()[0] == 0 and self.boutonEnfonce:
            self.boutonEnfonce = False
        self.affichage(screen)

    def affichage(self,screen):
        """Affiche le bouton à sa position."""
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
cyclej=10
cyclev=50
class Jeton(Bouton):        
    def action(self,screen):
        """Ajoute la valeur du jeton à la mise et démarre automatiquement le jeu."""
        global mise, jetonsDisponibles, paris, message, revele, animation_terminee
        animation_terminee = False
        paris.clear()
        if jetonsDisponibles >= self.valeur:
            mise += self.valeur
            jetonsDisponibles -= self.valeur
            revele = False
            melanger_gobelets_animation(screen,nombre_cycles=cyclej, rapidite=cyclev)
            message=""
        animation_terminee = True

def afficher_message(message, y_offset,screen):
    """Affiche un message en utilisant une couleur blanche et la police définie."""
    texte = police.render(message, True, WHITE)
    rect = texte.get_rect(center=(fond_largeur // 2, fond_hauteur // 2 - 150 + y_offset))
    screen.blit(texte, rect)
    

def afficher_jetons(screen):
    texte_jetons = police.render(f"{jetonsDisponibles}", True, WHITE)
    texte_mise = police.render(f"{mise}", True, WHITE)
    screen.blit(texte_jetons, (140, 44))
    screen.blit(texte_mise, (835, 44))

def melanger_gobelets_animation(screen,nombre_cycles=1, rapidite=1):
    """Anime plusieurs cycles de mélange des gobelets."""
    global gobelets_positions, bille_index, gobelets_ouverts, animation_terminee, message
    
    animation_terminee = False

    gobelets_ouverts = [False, False, False] 
    message = "" 

    for _ in range(nombre_cycles):
        nouvelles_positions = gobelets_positions[:]
        random.shuffle(nouvelles_positions)

        mapping = [(gobelets_positions[i], nouvelles_positions[i]) for i in range(3)]

        for step in range(rapidite):
            screen.blit(fond_image, (0, 0))
            for i, (pos_actuelle, pos_visee) in enumerate(mapping):
                x = pos_actuelle[0] + (pos_visee[0] - pos_actuelle[0]) * (step / rapidite)
                y = pos_actuelle[1] + (pos_visee[1] - pos_actuelle[1]) * (step / rapidite)
                screen.blit(gobelet_bas_image, (x, y))
                afficher_jetons(screen)
            pygame.display.flip()

        gobelets_positions = nouvelles_positions

    animation_terminee = True


def afficher_etat_initial(screen):
    """Affiche les gobelets ouverts avec la bille visible"""
    global gobelets_ouverts
    gobelets_ouverts = [True, True, True]

    screen.blit(fond_image, (0, 0))
    for i, pos in enumerate(gobelets_positions):
        screen.blit(gobelet_haut_image, pos)
        if i == bille_index:
            bille_x = pos[0] + gobelet_bas_image.get_width()
            bille_y = pos[1] + gobelet_bas_image.get_height()
            screen.blit(bille_image, (bille_x, bille_y))

billet_jeton5 = Jeton(5, "data/texture_gobelet/billet_5.png", 225,500)
billet_jeton25 = Jeton(25, "data/texture_gobelet/billet_25.png", 375,500)
billet_jeton50 = Jeton(50, "data/texture_gobelet/billet_50.png", 525,500)
billet_jeton100 = Jeton(100, "data/texture_gobelet/billet_100.png",675,500)

bouton_rect = bouton_image.get_rect(center=(500,420))
