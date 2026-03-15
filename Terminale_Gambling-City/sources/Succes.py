import pygame
from pygame.locals import *

class Succes:
    def __init__(self,chemin,x,y,scale):
        self.x = x
        self.y = y
        self.chemin = chemin
        self.image = pygame.image.load(self.chemin)
        self.image_sise = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.gagner = False

    def afficher(self,screen):
        if self.gagner == True:
            screen.blit(self.image_sise,(self.x,self.y))

