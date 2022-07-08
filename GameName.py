
import pygame
import asyncio
import math

from scripts.player import Player
from scripts.tile import Tile
from scripts.gui import Text, GuiManager
from scripts.images import *
from scripts.particle import Particle, ParticleManager
from scripts.enemy import Worm, Fly
from scripts.portal import Portal
from scripts.dimension_transition import dimTrans
from scripts.bullet import Bullet
from scripts.display import screen
from scripts.bomb import Bomb
from scripts.enemy_bullet import EnemyBullet
from scripts.background_scroll import BackGround

import random
from typing import List

import json

import platform

if platform.platform() == 'emscripten':
    from perlin_noise.noise import PerlinNoise
else:
    from perlin_noise import PerlinNoise


class Game:
    FPS = 60
    def __init__(self):
        self.screen = screen
        self.display = pygame.Surface((200, 150))
        self.minimap = pygame.Surface((1200, 1000))
        self.background = pygame.Surface((200, 150), pygame.OPENGL)
        self.clock = pygame.time.Clock()


        self.global_time = 0

        self.running = True
        pygame.display.set_caption("Pygame Community Summer Jam")

        self.events = None

        self.key_presses = {"a": False, "d": False}

        self.particle_manager = ParticleManager()

        with open("assets/map/map.json", "rb") as file:
            map_data = json.load(file)
        self.tiles = []
        for tile in map_data["map"]:
            rect = pygame.Rect(tile[0], tile[1], tile[2], tile[3])

        self.player = Player(300, 400)

        self.gui_manager = GuiManager([]) 

        self.seed = random.randrange(-1000000, 1000000)
        self.enemies = []

        self.scale_x = 800
        self.scale_y = 600

        self.trails = []
        self.trail_cooldown =  0

        self.decorations = []
        self.bullets = []

        self.clicking = False
        self.shoot_cooldown = 0
        self.explosion_effects = []
        self.explosions = []
        self.bombs = []
        self.enemy_bullets = []
        random.seed(self.seed)

        self.backgroundImage = pygame.image.load('assets/images/backgrounds/background.png').convert()
        self.BackGround = BackGround(self.backgroundImage, pygame.Vector2(0, 0), self.player)

        self.screen_shake = 0
    

    def generate_map(self, noise_size, threshold):
        self.seed = random.randrange(-1000000, 1000000)
        self.tiles = []
        self.decorations = []
        self.enemies = []

        noise = PerlinNoise(octaves=8, seed=self.seed)
        noise = [[noise([i/noise_size[0], j/noise_size[1]]) 
        for j in range(noise_size[0])] for i in range(noise_size[1])]
        for y, row in enumerate(noise):
            for x, tile in enumerate(row):
                if tile > threshold and y > 4:
                    if tile < threshold + 0.4:
                        self.tiles.append(Tile((x*16, y*16, 16, 16), (100, 100, 100)))


        for i, tile in enumerate(self.tiles):
            if tile._collision:
                if pygame.Rect(tile.rect.x, tile.rect.y - 16, 16, 16) in self.tiles:
                    tile.neighbours.append(pygame.Rect(tile.rect.x, tile.rect.y - 16, 16, 16)) #top
                if pygame.Rect(tile.rect.x, tile.rect.y + 16, 16, 16) in self.tiles:
                    tile.neighbours.append(pygame.Rect(tile.rect.x, tile.rect.y + 16, 16, 16)) #bottom
                if pygame.Rect(tile.rect.x + 16, tile.rect.y, 16, 16) in self.tiles:
                    tile.neighbours.append(pygame.Rect(tile.rect.x + 16, tile.rect.y, 16, 16)) #right
                if pygame.Rect(tile.rect.x - 16, tile.rect.y, 16, 16) in self.tiles:
                    tile.neighbours.append(pygame.Rect(tile.rect.x - 16, tile.rect.y, 16, 16)) #left


                if pygame.Rect(tile.rect.x, tile.rect.y - 16, 16, 16) not in self.tiles:
                    if random.randrange(0, 10) == 5:
                        self.enemies.append(Worm(tile.rect.x, tile.rect.y-16, tile))
                    if random.randrange(0, 15) == 5:
                        self.enemies.append(Fly(tile.rect.x, tile.rect.y- 16))
                        
                    if random.randrange(0, 30) == 5:
                        self.decorations.append([mushroom_img, tile.rect.x, tile.rect.y-16, tile])
                    self.tiles[i].image = grassy_top
                if pygame.Rect(tile.rect.x, tile.rect.y + 16, 16, 16) not in self.tiles:
                    if random.randrange(0, 10) == 5:
                        self.decorations.append([spike_img, tile.rect.x, tile.rect.y+16, tile])
                    
    def render_map(self, display: pygame.Surface, tiles: List[Tile]) -> None:
        """
        Renders the games tiles
        """
        for tile in self.tiles:
            if (math.dist([self.player.rect.x, self.player.rect.y], [tile.rect.x, tile.rect.y]) < 150):
                display.blit(tile.image, (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y))
                pygame.draw.rect(self.minimap, (255, 255, 255), (tile.rect.x, tile.rect.y, 16, 16))
                #self.minimap.blit(tile.image, (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y))
                for bullet in self.bullets:
                    if pygame.Rect(bullet.x, bullet.y, 4, 4).colliderect(
                        pygame.Rect(tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y, 16, 16)
                    ):  
                        self.screen_shake += 1
                        for i in range(4):
                            self.explosions.append([tile.rect.x, tile.rect.y+random.randrange(-7, 7), random.randrange(-4, 4),random.randrange(-2, 7), 1, (143, 86, 59), False, .2, 100])
                        self.bullets.remove(bullet)
                    
                for bomb in self.bombs:
                    if pygame.Rect(bomb.x-self.player.camera.x+2, bomb.y-self.player.camera.y+2, 6, 6).colliderect(pygame.Rect(tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y, 16, 16)):
                        bomb.should_move_down = False
                        if not bomb.detonate:

                            bomb.tiles_to_remove.append(tile)

                            for _tile in tile.neighbours:
                                try:
                                    bomb.tiles_to_remove.append(_tile)
                                    for __tile in self.tiles[self.tiles.index(_tile)].neighbours:
                                        try:
                                            bomb.tiles_to_remove.append(__tile)
                                        except ValueError:
                                            pass
                                except ValueError:
                                    pass
                            bomb.countdown = 40

                        bomb.detonate = True

                for enemy in self.enemies:
                    if str(enemy) == "Worm":
                        if enemy.displaced:
                            if pygame.Rect(enemy.x-self.player.camera.x+8, enemy.y-self.player.camera.y+16, 3, 3).colliderect(pygame.Rect(tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y, 16, 16)):
                                enemy.tile = tile

    def glow(self, surf, host, pos, radius, offset=0):
        glow_width = abs(math.sin(offset)*25) + radius *2

        glow_img = light_img
        surf.blit(pygame.transform.scale(glow_img, (glow_width, glow_width)), (pos[0]-glow_width/2, pos[1]-glow_width/2), special_flags=pygame.BLEND_RGBA_ADD)

    async def main(self):
        self.generate_map((75, 50), 0.02)

        self.portal = Portal([0, 0])
        self.portal.place_portal([10, 10], [65, 40], 16, self.tiles)
        self.player.camera = pygame.Vector2(self.portal.position)

        self.dimTrans = dimTrans(pygame.Rect(0, 0, 200, 150))
        light_surf = self.display.copy()
        

        while self.running:

            self.display.fill((34, 32, 52))
            self.minimap.fill((0, 0, 0))
            self.minimap.set_colorkey((0, 0,0))
            pygame.display.set_caption(f"{self.clock.get_fps()}")

            self.display.blit(pygame.transform.scale(self.background, (self.scale_x, self.scale_y)), (0, 0))

            self.BackGround.draw(self.display)

            self.global_time += 1
            display = self.display
            
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.is_on_ground:
                            self.player.y_velocity -= self.player.JUMP_HEIGHT
                            self.player.jump_count += 1
                            for i in range(15):
                                self.particle_manager.particles.append(Particle(self.player.rect.x, self.player.rect.y, random.randrange(5, 10), random.randrange(-3, 3), 0, True, random.randrange(3, 6), True))
                        if not self.player.is_on_ground and self.player.jump_count < 2:
                            self.player.y_velocity = 1
                            self.player.y_velocity -= self.player.JUMP_HEIGHT 
                            self.player.jump_count += 1
                            self.player.double_jumping = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        self.player.SPEED += 1
                        if not self.player.attacking:
                            self.player.attacking = True

                        self.player.dash = 15

                    if event.button == 3:
                        self.bombs.append(Bomb(self.player.rect.x, self.player.rect.y, int(self.player.moving_right)))
                        

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                        self.player.SPEED -= 1

            if self.clicking:
                if self.shoot_cooldown <= 0:
                        mx, my = pygame.mouse.get_pos()
                        mx /= 4
                        my /= 4

                        mx += random.randrange(-10, 10)
                        my += random.randrange(-10, 10)


                        rel_x, rel_y = mx - (self.player.rect.x-self.player.camera.x), my - (self.player.rect.y-self.player.camera.y)

                        self.bullets.append(Bullet(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y, mx, my, rel_x, rel_y))
                        self.shoot_cooldown = 10
                else:
                    self.shoot_cooldown -= 1

            keys = pygame.key.get_pressed()
            self.key_presses["a"] = keys[pygame.K_a]
            self.key_presses["d"] = keys[pygame.K_d]

            if self.player.SPEED  == 3:
                if self.trail_cooldown <= 0:
                    self.trails.append([self.player.walk_images[0].copy(), self.player.rect.x, self.player.rect.y,155])
                    self.trail_cooldown = 5
                else:
                    self.trail_cooldown -= 1

            if self.player.dash > 0:
                self.player.dash -= 1

            self.portal.draw(self.display, self.player.camera)
            
            self.portal.player_attract(self.player)
            self.portal.draw(self.minimap, pygame.math.Vector2(0, 0))

            self.player.handle_movement(self.key_presses, self.tiles)
            self.player.draw(self.display)
           # self.minimap.blit(
            #    pygame.transform.scale(
             #       pygame.transform.rotate(pygame.transform.flip(self.player.walk_images[self.player.animation_index//15], not self.player.moving_right, False), self.player.rotation), (32, 32)), (self.player.rect.x, self.player.rect.y))
            pygame.draw.circle(self.minimap, (255, 0, 0), (self.player.rect.x, self.player.rect.y), 15)

            for enemy in self.enemies:  
                if str(enemy) == "Worm":
                    if self.player.cooldown != 0:
                        if pygame.Rect(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y, self.player.rect.width, 
                            self.player.rect.height).colliderect(
                            pygame.Rect(enemy.x-self.player.camera.x, enemy.y-self.player.camera.y, 32, 32)
                        ):
                            
                            enemy.health -= 1

                    if enemy.bullet_cooldown <= 0 and math.dist([self.player.rect.x, self.player.rect.y], [enemy.x, enemy.y]) < 50:
                        x = enemy.x-self.player.camera.x
                        y = enemy.y-self.player.camera.y
                        px = self.player.rect.x-self.player.camera.x+random.randrange(-30, 30)
                        py = self.player.rect.y-self.player.camera.y+random.randrange(-30, 30)


                        angle = math.atan2(y-py, x-px)
                        x_vel = math.cos(angle) * 1
                        y_vel = math.sin(angle) * 1

                        self.enemy_bullets.append([enemy.x, enemy.y, [x_vel, y_vel], 400])
                        enemy.bullet_cooldown = 40
                    else:
                        enemy.bullet_cooldown -= 1    
                    enemy.draw(self.display, self.player.camera, self.player, self)

            self.render_map(self.display, self.tiles)

            self.gui_manager.draw_gui_elements(self.display, self.events)
            self.particle_manager.manage_particles(self.display, self.player.camera)

            light_surf.fill((0, 0, 0))

            self.glow(light_surf, self.player, (self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y), 130)
            for enemy in self.enemies:  
                if str(enemy) != "Worm":
                    enemy.draw(self.display, self.player.camera, self.player, self)
            for decoration in self.decorations:
                if decoration[3] in self.tiles:
                    self.display.blit(decoration[0], (decoration[1]-self.player.camera.x, decoration[2]-self.player.camera.y))
            for trail in self.trails:
                if trail[3] < 0:
                    self.trails.remove(trail)
                trail[0].set_alpha(trail[3])
                trail[3] -= 5
                self.display.blit(trail[0], (trail[1]-self.player.camera.x, trail[2]-self.player.camera.y))

            for eff in self.explosion_effects:
                    eff[2] -= 1
                    if eff[2] <= 0:
                        self.explosion_effects.remove(eff)
                    pygame.draw.circle(display, (39, 39, 68), (eff[0]-self.player.camera.x,eff[1]-self.player.camera.y), 1)
            for part in self.explosions:
                    if part[7] <= 0:
                        self.explosions.remove(part)
                    part[1] -= part[3]*random.random()
                    if part[3] > -10:
                        part[3] -= .3
                    part[0] += part[2]*random.random()
                    part[4] += .01
                    part[7] -= .005
                    if part[6] is False:
                        self.explosion_effects.append([part[0], part[1], 10])
                    pygame.draw.circle(display, part[5], (part[0]-self.player.camera.x, part[1]-self.player.camera.y), part[4])

            for bomb in self.bombs:
                bomb.draw(self.display, self.player.camera)
                if bomb.countdown > 0:
                    bomb.countdown -= 1
                if bomb.countdown <= 0 and not bomb.should_move_down:
                    self.screen_shake += 10
                    for i in range(200):
                        self.explosions.append([bomb.x, bomb.y+random.randrange(-17, 17), random.randrange(-4, 4),random.randrange(-2, 7), 1, (143, 86, 59), False, .2, 100])
                    for tile in bomb.tiles_to_remove:
                        try:
                            self.tiles.remove(tile)
                        except ValueError:
                            pass
                    self.bombs.remove(bomb)

            for bullet in self.enemy_bullets:
                if bullet[3] <= 0:
                    self.enemy_bullets.remove(bullet)
                bullet[0] -= bullet[2][0]
                bullet[1] -= bullet[2][1]
                bullet[3] -= 1
                self.glow(light_surf, self.player, (bullet[0]-self.player.camera.x, bullet[1]-self.player.camera.y), 13)

                pygame.draw.circle(self.display, (154, 40, 53), (bullet[0]-self.player.camera.x, bullet[1]-self.player.camera.y), 4)


            self.display.blit(light_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            #transition between dimensions
            if self.player.rect.colliderect(self.portal.posRect) and not self.dimTrans.active:
                self.dimTrans.activize()
            
            if self.dimTrans.change_scene:
                self.dimTrans.change_scene = False
                self.generate_map((75, 50), 0.02)
                self.portal.place_portal([10, 10], [65, 40], 16, self.tiles)
                self.player.rect.topleft = (400, 300)

            self.dimTrans.draw(self.display)

            for bullet in self.bullets:
                bullet.main(self.display)        

            color = abs(math.sin(self.global_time / 100)) 
            _c = color * 10
            self.background.fill((_c, _c, _c))



            if self.screen_shake:
                    self.player.camera.x += random.randint(0, 8) - 4
                    self.player.camera.y += random.randint(0, 8) - 4

            if self.screen_shake > 0:
                    self.screen_shake -= 1

            self.screen.blit(pygame.transform.scale(self.display, (self.scale_x, self.scale_y)), (0, 0))
            self.screen.blit(pygame.transform.scale(self.minimap, (200, 150)), (0, 0))

            pygame.display.update()
            self.clock.tick(self.FPS)
            await asyncio.sleep(0)

    def run(self):
        asyncio.run(self.main())