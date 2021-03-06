import pygame
import math
from scripts.images import bullet_img

class EnemyBullet:
    def __init__(self, x, y, mouse_x, mouse_y, rel_x, rel_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 4
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed

        self.angle_rot = ((180 / math.pi) * -math.atan2(rel_y, rel_x))
    def main(self, display, camera):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        img = pygame.transform.rotate(bullet_img, self.angle_rot).convert()
        display.blit(img, (self.x-camera.x, self.y-camera.y))

#Will do this on 13.07.2022
class AutoTargetBullet(EnemyBullet):#it's also enemy bullet:)
    def __init__(self, x, y, mouse_x, mouse_y, rel_x, rel_y):
        super.__init__(self, x, y, mouse_x, mouse_y, rel_x, rel_y)

    def main(self, display, camera):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)
        img = pygame.transform.rotate(bullet_img, self.angle_rot).convert()
        display.blit(img, (self.x-camera.x, self.y-camera.y))