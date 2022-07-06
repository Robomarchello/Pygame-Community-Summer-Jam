import pygame
import random

from scripts.entity import Entity
from scripts.images import *

class Worm(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.looking_right = True

        self.timer = 10

        self.health = 25

        self.dir = [0, 0]

        self.has_died = False
        self.wait_time = 10
        self.has_reset = False

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

    def draw(self, display, camera, player, game):
        self.move()
        img = pygame.transform.flip(worm_walk_imgs[0], not self.looking_right, False).convert()
        img.set_colorkey((255, 255, 255))


        if self.health <= 0:
            if not self.has_died:

                
                if player.moving_right:
                    self.dir[0] = random.randrange(5, 10)
                    self.dir[1] = random.randrange(-5, 5)
                else:
                    self.dir[0] = random.randrange(-10, -5)
                    self.dir[1] = random.randrange(-5, 5) 

            self.has_died = True
            self.wait_time -= 1

        if self.wait_time < 0:

            self.has_reset = True
            self.x += self.dir[0] * 4
            self.y += self.dir[1] * 4
            game.trails.append([img.copy(), self.x, self.y,155])


        display.blit(img, (self.x-camera.x, self.y-camera.y))