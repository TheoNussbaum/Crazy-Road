import pygame
pygame.init()

class VoitureJoueur:
    def __init__(self, x, y):
        self.largeur = 50
        self.hauteur = 100
        self.x = x
        self.y = y
        self.vitesse = 5
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def deplacer(self, direction):
        self.x += direction * self.vitesse
        self.rect.x = self.x

    def dessiner(self, fenetre):
        pygame.draw.rect(fenetre, ROUGE, self.rect)