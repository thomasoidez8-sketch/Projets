import pygame
pygame.init()

def get_events():
    """Renvoie la liste des événements en cours."""
    return pygame.event.get()