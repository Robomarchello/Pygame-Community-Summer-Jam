import pygame
import random
import math

from scripts.entity import Entity
from scripts.images import * 

class Skeleton(Entity):
    def __init__(self, x, y, tile):
        super().__init__(x, y)

        self.walk_imgs = [self.load_image("dungeon_cave/skeleton_walk1"), self.load_image("dungeon_cave/skeleton_walk2"), 
            self.load_image("dungeon_cave/skeleton_walk3"), self.load_image("dungeon_cave/skeleton_walk4"), 
            self.load_image("dungeon_cave/skeleton_walk5"), self.load_image("dungeon_cave/skeleton_walk6")]

        self.attack_imgs = [
            self.load_image("dungeon_cave/skeleton_attack1"), self.load_image("dungeon_cave/skeleton_attack2"), 
            self.load_image("dungeon_cave/skeleton_attack3"), self.load_image("dungeon_cave/skeleton_attack4"), 
            self.load_image("dungeon_cave/skeleton_attack5"), self.load_image("dungeon_cave/skeleton_attack6")
        ]

        self.health = 10
        self.hitcooldown = 0
        self.animation_index = 0

        self.tile = tile

        self.image = None

        self.collisions = []

        self.timer =  0
        self.moving_right = random.choice([True, False])

        self.attack_cooldown = 0
        self.attacking = True

        self.bullet_cooldown = 0

        self.displaced = False

    def __repr__(self):
        return "Skeleton"

    def draw(self, display, camera, player, game):
        if self.tile not in game.tiles:
            self.y += 1.5
            self.displaced = True
        else:
            self.displaced = False

        if self.timer <= 0:
            self.moving_right = not self.moving_right
            self.timer = 40
        else:
            self.timer -= 1
        if random.randrange(0, 3) == 2:
            if self.moving_right:
                self.x += 0.1
            else:
                self.x -= 0.1

        if self.bullet_cooldown <= 0 and math.dist([player.rect.x, player.rect.y], [self.x, self.y]) < 50:
            for i in range(5):
                x = self.x-camera.x + 5
                y = self.y-camera.y
                px = player.rect.x-camera.x+random.randrange(-60, 60)
                py = player.rect.y-camera.y+random.randrange(-60, 60)

                angle = math.atan2(y-py, x-px)
                x_vel = math.cos(angle) * 1
                y_vel = math.sin(angle) * 1

                game.enemy_bullets.append([self.x, self.y, [x_vel, y_vel], 400])
            self.bullet_cooldown = random.randrange(10, 20)
        else:
            self.bullet_cooldown -= 1

        if self.attack_cooldown <= 0:
            self.attacking = not self.attacking
            self.attack_cooldown = 60
        else:
            self.attack_cooldown -= 1

        self.animation_index = self.animate(self.walk_imgs, self.animation_index, 5)
        if self.hitcooldown > 0:
            self.hitcooldown -= 1
        if self.hitcooldown == 0:
            if not self.attacking:
                self.image = self.walk_imgs[self.animation_index // 5]
            else:
                self.image = self.attack_imgs[self.animation_index // 5]

        display.blit(pygame.transform.flip(self.image, not self.moving_right, False), (self.x - camera.x, self.y - camera.y))

        

class Fly(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.images = [self.load_image("fly1"), self.load_image("fly2"), self.load_image("fly3")]
        self.animation_index = 0
        
        self.rect = None
        self.image = None

        self.hitcooldown = 0

        self.bullet_cooldown = 0

        self.health = 6

        self.bullet_patterns = [[0.5, 0], [-0.5, 0], [0, 0.5], [0, -0.5], [0.25, 0.25], [-0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]

    def __repr__(self):
        return "Fly"

    def draw(self, display, camera, player, game):
        if math.dist([self.x, self.y], [player.rect.x, player.rect.y]) < 100:
            self.rect = pygame.Rect(self.x-camera.x, self.y-camera.y, 16, 16)
            movement_vector = self.move_towards(player.rect.x-camera.x + random.randrange(-90, 90), player.rect.y-camera.y + random.randrange(-90, 90), 1)
            self.x += movement_vector[0] 
            self.y += movement_vector[1] 
            if self.bullet_cooldown <= 0:
                for pattern in self.bullet_patterns:
                    game.enemy_bullets.append([self.x, self.y, pattern, 400])
                self.bullet_cooldown = random.randrange(80, 100)
            else:
                self.bullet_cooldown -= 1
            

        if self.hitcooldown > 0:
            self.hitcooldown -= 1
        if self.hitcooldown == 0:
            self.image = self.images[self.animation_index // 15]

        self.animation_index = self.animate(self.images, self.animation_index, 15)
        display.blit(self.image, (self.x - camera.x, self.y - camera.y))

class Worm(Entity):
    def __init__(self, x, y, tile):
        super().__init__(x, y)

        self.looking_right = True

        self.timer = 10

        self.health = 4

        self.dir = [0, 0]

        self.has_died = False
        self.wait_time = 10
        self.has_reset = False
        self.tile = tile

        self.y_vel = 4

        self.displaced = False

        self.bullet_cooldown = 0

        self.img = None
        self.image = worm_walk_imgs[0]

        self.hitcooldown = 0

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
        self.img = pygame.transform.flip(self.image, not self.looking_right, False).convert()
        self.img.set_colorkey((255, 255, 255))
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
        
        if self.hitcooldown > 0:
            self.hitcooldown -= 1
        if self.hitcooldown == 0:
            self.image = worm_walk_imgs[0]

        display.blit(pygame.transform.flip(self.image, not self.looking_right, False), (self.x-camera.x, self.y-camera.y))