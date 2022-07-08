import pygame
import random
import math

from scripts.entity import Entity
from scripts.images import *

class Fly(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.images = [self.load_image("fly1"), self.load_image("fly2"), self.load_image("fly3")]
        self.animation_index = 0
        
        self.rect = None

    def __repr__(self):
        return "Fly"

    def draw(self, display, camera, player, game):
        if math.dist([self.x, self.y], [player.rect.x, player.rect.y]) < 100:
            self.rect = pygame.Rect(self.x-camera.x, self.y-camera.y, 16, 16)
            movement_vector = self.move_towards(player.rect.x-camera.x, player.rect.y-camera.y, 1)
            self.x += movement_vector[0] 
            self.y += movement_vector[1] 

        self.animation_index = self.animate(self.images, self.animation_index, 15)
        display.blit(self.images[self.animation_index // 15], (self.x - camera.x, self.y - camera.y))

class Worm(Entity):
    def __init__(self, x, y, tile):
        super().__init__(x, y)

        self.looking_right = True

        self.timer = 10

        self.health = 25

        self.dir = [0, 0]

        self.has_died = False
        self.wait_time = 10
        self.has_reset = False
        self.tile = tile

        self.y_vel = 4

        self.displaced = False

        self.bullet_cooldown = 0

    def __repr__(self):
        return "Worm"

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
        if self.tile not in game.tiles:
            self.x += 4
            self.y -= self.y_vel
            self.y_vel -= 1
            self.displaced = True
        else:
            self.displaced = False

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