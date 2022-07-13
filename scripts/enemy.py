import pygame
import random
import math

from scripts.entity import Entity
from scripts.images import * 

class Boss(Entity):
    def __init__(self, x, y, target_y):
        super().__init__(x, y)

        self.health = 20
        self.target_y = target_y

        self.images = [self.load_image("green_cave/boss1"), self.load_image("green_cave/boss2"), self.load_image("green_cave/boss3")]

        self.image = None
        self.animation_index = 0
        self.hitcooldown = 0

        self.state = 0
        self.right = True
        self.change_cooldown = 0

        self.degree = 0

        self.bullet_cooldown = 0

    def __repr__(self):
        return "Boss"

    def cutscene(self, game):
        if game.boss_cut_scene:
            if self.y < self.target_y:
                self.y += 1
                game.glow_size = 200
            else:
                game.player.camera.y += 10
                game.glow_size = 90
                game.boss_cut_scene  = False

    def draw(self, display, camera, player, game):
        self.cutscene(game)

        if self.state == 0:
            #if self.right:
             #   self.x += 1

            #else:
             #   self.x -= 1

            if self.change_cooldown <= 0:
                self.right = not self.right
                self.change_cooldown = 60
            else:
                self.change_cooldown -= 1

            if self.bullet_cooldown <= 0:
                xradius = 200
                yradius = 100
                x1 = int(math.cos(self.degree*2*math.pi/360)*xradius)+300
                y1 = int(math.sin(self.degree*2*math.pi/360)*xradius)+150
                #pygame.draw.circle(display, RED, (x1-scroll[0]-100,y1-scroll[1]), 5)
                target_x = x1-camera.x
                target_y = y1-camera.y
                angle = math.atan2((self.y-camera.y)-target_y, (self.x-camera.x)-target_x)
                x_vel = math.cos(angle) * 3
                y_vel = math.sin(angle) * 3
                
                bullet = [x_vel, y_vel]

                game.enemy_bullets.append([self.x + 16, self.y + 16, bullet, 400, 0])
                self.degree+=2

                self.bullet_cooldown = 3
            else:
                self.bullet_cooldown -= 1

        if self.hitcooldown > 0:
            self.hitcooldown -= 1
        if self.hitcooldown == 0:
            self.image = self.images[self.animation_index // 15]

        self.animation_index = self.animate(self.images, self.animation_index, 15)

        display.blit(self.image, (self.x-camera.x, self.y-camera.y))
class GreenBat(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.images = [self.load_image("green_cave/bat_fly1"), self.load_image("green_cave/bat_fly2"), self.load_image("green_cave/bat_fly3"), self.load_image("green_cave/bat_fly4")]
        self.animation_index = 0

        self.health = 8

        self.image = None

        self.hitcooldown = 0
        self.bullet_cooldown = 0

        self.bullet_patterns = [                    [0, 1], [0, -1], 

                    [0.8, 0.8], [-0.8, 0.8], 
                    [-0.8, -0.8], [0.8, -0.8]]

        self.offset_x = random.randrange(-90, 90)
        self.offset_y = random.randrange(-90, 90)

        self.offset_reset_cooldown = 0


    def __repr__(self):
        return "GreenBat"

    def draw(self, display, camera, player, game):
        if math.dist([self.x, self.y], [player.rect.x, player.rect.y]) < 100:
            self.rect = pygame.Rect(self.x-camera.x, self.y-camera.y, 16, 16)
            movement_vector = self.move_towards(player.rect.x-camera.x + self.offset_x, player.rect.y-camera.y + self.offset_y, 1)
            self.x += movement_vector[0] 
            self.y += movement_vector[1] 
            if self.bullet_cooldown <= 0:
                for pattern in self.bullet_patterns:
                    game.enemy_bullets.append([self.x, self.y, pattern, 400])
                self.bullet_cooldown = random.randrange(80, 100)
            else:
                self.bullet_cooldown -= 1

        if self.offset_reset_cooldown <= 0:
            self.offset_x = random.randrange(-90, 90)
            self.offset_y = random.randrange(-90, 90)
            self.offset_reset_cooldown = 40
        else:
            self.offset_reset_cooldown -= 1

        if self.hitcooldown > 0:
            self.hitcooldown -= 1
        if self.hitcooldown == 0:
            self.image = self.images[self.animation_index // 15]

        self.animation_index = self.animate(self.images, self.animation_index, 15)
        display.blit(self.image, (self.x - camera.x, self.y - camera.y))

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

        self.health = 7
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
            self.bullet_cooldown = random.randrange(30, 45)
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

class LavaCrab(Entity):
    def __init__(self, x, y, tile, lookDir, LavaLen, lavaPillar):
        super().__init__(x, y)
        self.lavaPillar = lavaPillar

        self.velocity = pygame.Vector2(0, 1)
        self.moveDir = {'up': False, 'down': False}

        self.timer = 10

        self.health = 2

        self.has_died = False
        self.wait_time = 10
        self.has_reset = False
        self.tile = tile

        self.y_vel = 4

        self.displaced = False

        self.bullet_cooldown = 0

        self.img = None
        self.image = pygame.transform.flip(LavaCrabImg, lookDir, False)

        self.rect = self.image.get_rect(topleft=(x, y))

        self.LavaLen = LavaLen

        self.MinY = self.rect.copy().y + 16
        self.MaxY = self.rect.copy().y + (16 * LavaLen)

        self.rect.y += 16

        self.hitcooldown = 0
        self.bullet_patterns = [[0.5, 0], [-0.5, 0], [0, 0.5], [0, -0.5], [0.25, 0.25], [-0.25, 0.25], [0.25, -0.25], [-0.25, -0.25]]

        self.CamRect = pygame.Rect
        

    def __repr__(self):
        return "LavaCrab"

    def ChangeDir(self, camera, game):      
        if self.rect.y < self.MinY or self.rect.y > self.MaxY:
            self.velocity *= -1

    def move(self, camera, game):
        self.rect.topleft += self.velocity

        self.ChangeDir(camera, game)

    def draw(self, display, camera, player, game):
        if self.tile not in game.tiles:
            self.displaced = True
        else:
            self.displaced = False

        self.move(camera, game)

        self.img = self.image
        self.img.set_colorkey((255, 255, 255))

        self.CamRect = self.rect.copy()
        self.CamRect.topleft -= pygame.Vector2(camera.x, camera.y)

        if math.dist([self.rect.x, self.rect.y], [player.rect.x, player.rect.y]) < 100:
            if self.bullet_cooldown <= 0:
                for pattern in self.bullet_patterns:
                    game.enemy_bullets.append([self.rect.x, self.rect.y, pattern, 400])
                self.bullet_cooldown = 300
            else:
                self.bullet_cooldown -= 1

        display.blit(self.image, self.CamRect.topleft)

class MagicOrb(Entity):
    def __init__(self, x, y, tile):
        super().__init__(x, y)

        self.health = 5
        self.tile = tile

        self.image = MagicOrbImage
        self.rect = self.image.get_rect(topleft=(x, y))

        self.collisions = []

        self.bullet_cooldown = 0

        self.displaced = False

    def __repr__(self):
        return "MagicOrb"

    def draw(self, display, camera, player, game):
        if self.tile not in game.tiles:
            self.displaced = True
        else:
            self.displaced = False

        distance = math.dist([player.rect.x, player.rect.y], [self.x, self.y])
        
        if self.bullet_cooldown <= 0 and distance < 250:
            for i in range(5):
                x = self.x-camera.x + 5
                y = self.y-camera.y
                px = player.rect.x-camera.x+random.randrange(-60, 60)
                py = player.rect.y-camera.y+random.randrange(-60, 60)

                angle = math.atan2(y-py, x-px)
                x_vel = math.cos(angle) * 1
                y_vel = math.sin(angle) * 1

                game.enemy_bullets.append([self.x, self.y, [x_vel, y_vel], 400])
            self.bullet_cooldown = random.randrange(30, 45)
        else:
            self.bullet_cooldown -= 1

        display.blit(self.image, (self.x - camera.x, self.y - camera.y))
