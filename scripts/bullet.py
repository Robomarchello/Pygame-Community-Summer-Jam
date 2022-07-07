import pygame
import math
from scripts.images import bullet_img

class Bullet:
    def __init__(self, x, y, mouse_x, mouse_y, rel_x, rel_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 10
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

        self.angle_rot = ((180 / math.pi) * -math.atan2(rel_y, rel_x))
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        img = pygame.transform.rotate(bullet_img, self.angle_rot).convert()
        display.blit(img, (self.x, self.y))