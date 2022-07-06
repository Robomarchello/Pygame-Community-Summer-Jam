import pygame
import asyncio
import math

from scripts.player import Player
from scripts.tile import Tile
from scripts.gui import Text, GuiManager
from scripts.images import *
from scripts.particle import Particle, ParticleManager
from scripts.enemy import Worm
from scripts.portal import Portal

import random
from typing import List

import json
from perlin_noise import PerlinNoise

class Game:
    FPS = 60
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((800, 600))
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

        self.tx = 100
        self.ty = 100

        self.enemies = []

        self.scale_x = 800
        self.scale_y = 600

        self.trails = []
        self.trail_cooldown =  0


        
    def generate_map(self, noise_size, threshold):
        noise = PerlinNoise(octaves=8, seed=self.seed)
        noise = [[noise([i/noise_size[0], j/noise_size[1]]) 
        for j in range(noise_size[0])] for i in range(noise_size[1])]
        for y, row in enumerate(noise):
            for x, tile in enumerate(row):
                if tile > threshold:
                    rect = pygame.Rect(x*16, y*16, 16, 16)
                    self.tiles.append(Tile(rect=rect, color=(100, 100, 100), image="assets/images/example.png"))

        for i, tile in enumerate(self.tiles):
            if pygame.Rect(tile.rect.x, tile.rect.y - 16, 16, 16) not in self.tiles:
                if random.randrange(0, 10) == 5:
                    self.enemies.append(Worm(tile.rect.x, tile.rect.y-16))
                self.tiles[i].image = pygame.image.load("assets/images/grassy_caves/top.png")

    def render_map(self, display: pygame.Surface, tiles: List[Tile]) -> None:
        """
        Renders the games tiles
        """

        for tile in tiles:
            display.blit(tile.image, (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y))


    def glow(self, surf, host, pos, radius, offset=0):
        if host:
            timing_offset = (hash(host) / 1000) % 1
            timing_offset += 1
        else:
            timing_offset = 0
        glow_width = abs(math.sin(self.global_time+offset)*25) + radius *2

        glow_img = light_img
        surf.blit(pygame.transform.scale(glow_img, (glow_width, glow_width)), (pos[0]-glow_width/2, pos[1]-glow_width/2), special_flags=pygame.BLEND_RGBA_ADD)

    async def main(self):
        self.generate_map((75, 50), 0.02)

        self.portal = Portal([0, 0])
        self.portal.place_portal([10, 10], [65, 40], 16, self.tiles)
        self.player.camera = pygame.Vector2(self.portal.position)
        while self.running:
            self.display.fill((34, 32, 52))
            pygame.display.set_caption(f"{self.clock.get_fps()}")
            
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
                            self.player.y_velocity -= self.player.JUMP_HEIGHT 
                            self.player.jump_count += 1
                            self.player.double_jumping = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.SPEED += 3
                        if not self.player.attacking:
                            self.player.attacking = True

                        self.player.dash = 15

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.SPEED -= 3

            keys = pygame.key.get_pressed()
            self.key_presses["a"] = keys[pygame.K_a]
            self.key_presses["d"] = keys[pygame.K_d]

            if self.player.SPEED  == 5:
                if self.trail_cooldown <= 0:
                    self.trails.append([self.player.walk_images[0].copy(), self.player.rect.x, self.player.rect.y,155])
                    self.trail_cooldown = 5
                else:
                    self.trail_cooldown -= 1

            if self.player.dash > 0:
                self.player.dash -= 1

                


           # px = self.player.rect.x - self.player.camera.x
            #px = self.player.rect.x - self.player.camera.x






            self.portal.draw(self.display, self.player.camera)

            self.player.handle_movement(self.key_presses, self.tiles)
            self.player.draw(self.display)

            self.render_map(self.display, self.tiles)

            self.gui_manager.draw_gui_elements(self.display, self.events)
            self.particle_manager.manage_particles(self.display, self.player.camera)

            
            
            light_surf = self.display.copy()
            light_surf.fill((0, 0, 0))

            self.glow(light_surf, self.player, (self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y), 130)
            for enemy in self.enemies:  
                if self.player.cooldown != 0:
                    if pygame.Rect(self.player.rect.x-self.player.camera.x, self.player.rect.y-self.player.camera.y, self.player.rect.width, 
                        self.player.rect.height).colliderect(
                        pygame.Rect(enemy.x-self.player.camera.x, enemy.y-self.player.camera.y, 32, 32)
                    ):


                        enemy.health -= 1
                enemy.draw(self.display, self.player.camera, self.player, self)
            for trail in self.trails:
                if trail[3] < 0:
                    self.trails.remove(trail)
                trail[0].set_alpha(trail[3])
                trail[3] -= 5
                self.display.blit(trail[0], (trail[1]-self.player.camera.x, trail[2]-self.player.camera.y))
          #  self.display.blit(light_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.screen.blit(pygame.transform.scale(self.display, (self.scale_x, self.scale_y)), (0, 0))
            
            self.screen.blit(pygame.transform.scale(self.display, (800, 600)), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)
            await asyncio.sleep(0)

    def run(self):
        asyncio.run(self.main())
