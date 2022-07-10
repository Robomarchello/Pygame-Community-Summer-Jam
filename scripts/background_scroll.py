import pygame
from copy import copy


pygame.init()

class BackGround():
    def __init__(self, background, offset:pygame.Vector2, player):
        self.background = background
        self.offset = offset
        self.player = player

    def draw(self, screen):
        position = self.get_position()
        screen.blit(self.background, position)

    def get_position(self):
        position = copy(self.offset)
        position -= self.player.camera

        return position