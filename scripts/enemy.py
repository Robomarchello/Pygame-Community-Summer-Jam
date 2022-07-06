import pygame
import random

from scripts.entity import Entity
from scripts.images import *

class Worm(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.looking_right = True

        self.timer = 10

    def move(self):
        if random.randrange(0, 15) == 5:
            if self.looking_right:
                self.x += .5
            else:
                self.x -= .5

            self.timer -= 1
            if self.timer <= 0:
                self.looking_right = not self.looking_right
                self.timer = 10

        



    def draw(self, display, camera):
        self.move()
        display.blit(pygame.transform.flip(worm_walk_imgs[0], not self.looking_right, False).convert(), (self.x-camera.x, self.y-camera.y))