import pygame

from scripts.entity import Entity

class Bomb(Entity):
    def __init__(self, x, y, direction):
        super().__init__(x, y)

        self.direction = direction
        self.y_vel = -4
        self.should_move_down = True
        self.animation_index = 0
        self.countdown = 0
        self.images = [self.load_image("bomb1"), self.load_image("bomb2")]
        self.detonate = False
        self.tiles_to_remove = []
        self.should_play_click_sound_cooldown = 0
        self.lifetime = 100

    def draw(self, display, camera):
        self.lifetime -= 1
        self.y_vel += 0.3
        if self.should_move_down:
            self.y += self.y_vel
            if self.direction:
                self.x += 3
            else:
                self.x -= 3

        self.animation_index = self.animate(self.images, self.animation_index, 15)
        display.blit(self.images[self.animation_index//15], (self.x-camera.x, self.y-camera.y))