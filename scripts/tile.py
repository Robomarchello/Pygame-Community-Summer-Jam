import pygame

from scripts.images import *

class Tile:
    def __init__(self, rect, color):
        self.color = color
        self.image = base
        self.image.set_colorkey((255, 255, 255))
        self.rect = pygame.Rect(rect)
        self._collision = True
        self.neighbours = []

    def collision(self, player_rect: pygame.Rect) -> bool:
        return player_rect.colliderect(self.rect)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))