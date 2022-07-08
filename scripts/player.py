from typing import List

import pygame
import math

from scripts.entity import Entity
from scripts.tile import Tile
from scripts.particle import Particle
from scripts.images import *

class Player(Entity):
    JUMP_HEIGHT = 7

    def __init__(self, x, y) -> None:
        super().__init__(x, y)
         
        self.y_velocity = 3
        self.is_on_ground = False
        self.rect = pygame.Rect(self.x, self.y, 16, 16)

        self.walk_images = [self.load_image("player_walk1"), self.load_image("player_walk2"), self.load_image("player_walk3")]
        self.idle_images = [
            self.load_image("player_idle1"), self.load_image("player_idle2"), self.load_image("player_idle1")
        ]
        self.animation_index = 0
        
        self.camera = pygame.math.Vector2()
        self.player_movement = {"horizontal": 0, "vertical": self.y_velocity}

        self.jump_count = 0

        self.SPEED = 2

        self.attacking = False

        self.spear_offset = 5
        self.cooldown = 0

        self.moving_right = True

        self.dash = 0
        self.rotation = 0
        self.double_jumping = False

        self.moving = False

    def get_colliding_tiles(
        self, tiles: List[Tile], player_rect: pygame.Rect
    ) -> List[Tile]:
        """
        Returns a list of tiles the player is currently colliding with
        """
        return_tiles = []
        for tile in tiles:
            if tile._collision:
                if (math.dist([self.rect.x, self.rect.y], [tile.rect.x, tile.rect.y]) < 25):
                    return_tiles.append(tile)

        return return_tiles

    def calculate_rect(
        self, movement: dict, player_rect: pygame.Rect, map_tiles: List[Tile]
    ) -> pygame.Rect:
        """
        Calculates the Rect of the player based on their movement and the surrounding tiles
        """
        player_rect.x += movement["horizontal"]
        tiles = self.get_colliding_tiles(map_tiles, player_rect)
        for tile in tiles:
            if tile.collision(player_rect):
                if movement["horizontal"] > 0:
                    player_rect.right = tile.rect.left
                if movement["horizontal"] < 0:
                    player_rect.left = tile.rect.right

        self.is_on_ground = False
        player_rect.y += movement["vertical"]
        for tile in tiles:
            if tile.collision(player_rect):
                if movement["vertical"] > 0:
                    player_rect.bottom = tile.rect.top
                    self.is_on_ground = True
                    self.y_velocity = 2
                    self.jump_count = 0
                    self.double_jumping = False
                    self.rotation = 0
                if movement["vertical"] < 0:
                    player_rect.top = tile.rect.bottom

        return player_rect

    def handle_movement(self, key_presses: dict, tiles) -> pygame.Rect:
        """
        Handles all code relating to the movement of the player
        """

        self.player_movement = {"horizontal": 0, "vertical": self.y_velocity}

        if key_presses["a"]:
            self.moving = True
            self.player_movement["horizontal"] -= self.SPEED
            self.moving_right = False
        if key_presses["d"]:
            self.moving = True
            self.player_movement["horizontal"] += self.SPEED
            self.moving_right = True


        if self.y_velocity < 3:
            self.y_velocity += 0.2

        self.rect = self.calculate_rect(self.player_movement, self.rect, tiles)

    def get_pos(self):
        return (self.x-self.camera.x, self.y-self.camera.y)

        
        

    def draw(self, display) -> None:
        """
        Draws the player at the rect position
        """
        mx, my = pygame.mouse.get_pos()
        mx /= 2
        self.camera.x += (self.rect.x-self.camera.x-80+mx/50)/7
        self.camera.y += (self.rect.y-self.camera.y-75+my/50)/7

        if self.attacking:
            self.cooldown = 10
            self.attacking = False

        if self.cooldown > 0:
            if self.cooldown >= 5:
                self.spear_offset += 1
            else:
                self.spear_offset -= 1
            self.cooldown -= 1
        else:
            self.spear_offset = 5

        if self.double_jumping:
            self.rotation += 10

        self.animation_index = self.animate(self.walk_images, self.animation_index, 15)
        if self.moving:
            display.blit(pygame.transform.rotate(pygame.transform.flip(self.walk_images[self.animation_index//15], not self.moving_right, False), self.rotation), (self.rect.x-self.camera.x, self.rect.y-self.camera.y))
        else:
            display.blit(pygame.transform.rotate(pygame.transform.flip(self.idle_images[self.animation_index//15], not self.moving_right, False), self.rotation), (self.rect.x-self.camera.x, self.rect.y-self.camera.y))

        mx, my = pygame.mouse.get_pos()
        mx /= 4
        my /= 4
        px = pygame.Rect(self.rect.x-self.camera.x, self.rect.y-self.camera.y, self.rect.width, self.rect.height).centerx
        py = pygame.Rect(self.rect.x-self.camera.x, self.rect.y-self.camera.y, self.rect.width, self.rect.height).centery
       
        dx, dy = mx - px, my - py
        angle = math.degrees(math.atan2(-dy, dx)) - 0

        rot_image = pygame.transform.rotate(spear_img, angle).convert()
        rot_image.set_colorkey((255, 255, 255))
        rot_image_rect = rot_image.get_rect()
        rot_image_rect.center = pygame.Rect(self.rect.x-self.camera.x, self.rect.y-self.camera.y + 2, self.rect.width, self.rect.height).center
        display.blit(rot_image, rot_image_rect.topleft)
        self.moving = False