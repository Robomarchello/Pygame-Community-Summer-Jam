import pygame
import asyncio

from scripts.player import Player
from scripts.tile import Tile
from scripts.gui import Text, GuiManager
from scripts.images import *

import random
from typing import List

import json
from perlin_noise import PerlinNoise

class Game:
    FPS = 60
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((200, 150))
        self.clock = pygame.time.Clock()

        self.running = True
        pygame.display.set_caption("Pygame Community Summer Jam")

        self.events = None

        self.key_presses = {"a": False, "d": False}

        with open("assets/map/map.json", "rb") as file:
            map_data = json.load(file)
        self.tiles = []
        for tile in map_data["map"]:
            rect = pygame.Rect(tile[0], tile[1], tile[2], tile[3])

        self.player = Player(100, 100)

        self.gui_manager = GuiManager([Text(100, 100, "hello world", 32)]) 

    def generate_map(self, noise_size, threshold):
        noise = PerlinNoise(octaves=14, seed=1)
        noise = [[noise([i/noise_size[0], j/noise_size[1]]) 
        for j in range(noise_size[0])] for i in range(noise_size[1])]
        for y, row in enumerate(noise):
            for x, tile in enumerate(row):
                if tile > threshold:
                    rect = pygame.Rect(x*16, y*16, 16, 16)
                    self.tiles.append(Tile(rect=rect, color=(100, 100, 100), image="assets/images/example.png"))

    def render_map(self, display: pygame.Surface, tiles: List[Tile]) -> None:
        """
        Renders the games tiles
        """

        for tile in tiles:
            display.blit(tile.image, (tile.rect.x-self.player.camera.x, tile.rect.y-self.player.camera.y))


    async def main(self):
        self.generate_map((100, 75), 0.07)
        while self.running:
            self.display.fill((65, 106, 163))
            pygame.display.set_caption(f"{self.clock.get_fps()}")

            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.is_on_ground:
                            self.player.y_velocity -= self.player.JUMP_HEIGHT

            keys = pygame.key.get_pressed()
            self.key_presses["a"] = keys[pygame.K_a]
            self.key_presses["d"] = keys[pygame.K_d]

            self.player.handle_movement(self.key_presses, self.tiles)
            self.player.draw(self.display)

            self.render_map(self.display, self.tiles)

            self.gui_manager.draw_gui_elements(self.display, self.events)

            self.screen.blit(pygame.transform.scale(self.display, (800, 600)), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)
            await asyncio.sleep(0)

    def run(self):
        asyncio.run(self.main())
