import pygame
import time

pygame.init()

fond_image = pygame.image.load("data/texture_gobelet/plateaux_jeux_gobelet.png")
fond_image = pygame.transform.scale(fond_image, (1000, 600))

fond_largeur = fond_image.get_width()
fond_hauteur = fond_image.get_height()

WHITE = (255, 255, 255)

police = pygame.font.Font('data/fichiers_additionnels/Crang.ttf', 16)

jetonsDisponibles = 1000
mise = 0
message = ""

timer_active = False
start_time = 0

def definir_image_gobelet():
    """Définit l'image du gobelet selon la mise."""
    if mise > 0:
        return pygame.image.load("data/texture_gobelet/boite_fermer.png")
    else:
        return pygame.image.load("data/texture_gobelet/boite_ouverte.png")

bouton_image = pygame.transform.scale(definir_image_gobelet(), (200, 205))
bouton_rect = bouton_image.get_rect(center=(fond_largeur // 2, fond_hauteur // 2))

class Jeton:
    def __init__(self, valeur, cheminImage, posX, posY):
        self.image = pygame.transform.scale(pygame.image.load(cheminImage), (75, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX, posY)
        self.valeur = valeur
        self.boutonEnfonce = False
    
    def utilisation(self, screen):
        global mise, jetonsDisponibles, message, bouton_image
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.boutonEnfonce:
                self.boutonEnfonce = True
                if jetonsDisponibles >= self.valeur:
                    mise += self.valeur
                    jetonsDisponibles -= self.valeur
                    message = "Jeton misé !"
                    bouton_image = pygame.transform.scale(definir_image_gobelet(), (200, 205))
            
        if pygame.mouse.get_pressed()[0] == 0 and self.boutonEnfonce:
            self.boutonEnfonce = False
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

def afficher_message(message, y_offset,screen):
    texte = police.render(message, True, WHITE)
    rect = texte.get_rect(center=(fond_largeur // 2, fond_hauteur // 2 - 150 + y_offset))
    screen.blit(texte, rect)

def afficher_jetons(screen):
    texte_jetons = police.render(f"{jetonsDisponibles}", True, WHITE)
    texte_mise = police.render(f"{mise}", True, WHITE)
    screen.blit(texte_jetons, (140, 44))
    screen.blit(texte_mise, (835, 44))

def jouer():
    global mise, jetonsDisponibles, message, timer_active, start_time
    
    if mise == 0:
        message = "Misez avant de jouer !"
        return
    
    timer_active = True
    start_time = time.time()

billet_jeton5 = Jeton(5, "data/texture_gobelet/billet_5.png", 225, 500)
billet_jeton25 = Jeton(25, "data/texture_gobelet/billet_25.png", 375, 500)
billet_jeton50 = Jeton(50, "data/texture_gobelet/billet_50.png", 525, 500)
billet_jeton100 = Jeton(100, "data/texture_gobelet/billet_100.png", 675, 500)
