
import pygame
import os
from scripts.display import screen

def load_img(path, color=(255,255,255), base="font"):
    img = pygame.image.load(os.path.join("assets", base, f"{path}.png")).convert()
    img.set_colorkey(color)
    return img

light_img = load_img("light", base="images")
light_mask_full = pygame.transform.scale(light_img, (400, 300))
light_mask_full.blit(light_mask_full, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

spear_img = load_img("gun", base="images")
mushroom_img = load_img("mushroom1", base="images")
spike_img = load_img("spike", base="images")
bullet_img = load_img("bullet", base="images")
grassy_top = pygame.image.load("assets/images/grassy_caves/top.png").convert()
grassy_top.set_colorkey((255, 255, 255))
dungeon_top = pygame.image.load("assets/images/dungeon_cave/dungeon_top.png").convert()
dungeon_top.set_colorkey((255, 255, 255))
base = pygame.image.load("assets/images/example.png").convert()
base.set_colorkey((255, 255, 255))
grass_bg = pygame.image.load("assets/images/bg_tile.png").convert()
grass_bg.set_colorkey((255, 255, 255))

worm_walk_imgs = [load_img("worm_walk1", base="images"), load_img("worm_walk2", base="images"), load_img("worm_walk3", base="images")]
worm_hit_img = load_img("worm_hit", base="images")

alphabet = {
    "a": load_img("a", (0,0,0)),
    "b": load_img("b", (0,0,0)),
    "c": load_img("c", (0,0,0)),
    "d": load_img("d", (0,0,0)),
    "e": load_img("e", (0,0,0)),
    "f": load_img("f", (0,0,0)),
    "g": load_img("g", (0,0,0)),
    "h": load_img("h", (0,0,0)),
    "i": load_img("i", (0,0,0)),
    "j": load_img("j", (0,0,0)),
    "k": load_img("k", (0,0,0)),
    "l": load_img("l", (0,0,0)),
    "m": load_img("m", (0,0,0)),
    "n": load_img("n", (0,0,0)),
    "o": load_img("o", (0,0,0)),
    "p": load_img("p", (0,0,0)),
    "q": load_img("q", (0,0,0)),
    "r": load_img("r", (0,0,0)),
    "s": load_img("s", (0,0,0)),
    "t": load_img("t", (0,0,0)),
    "u": load_img("u", (0,0,0)),
    "v": load_img("v", (0,0,0)),
    "w": load_img("w", (0,0,0)),
    "x": load_img("x", (0,0,0)),
    "y": load_img("y", (0,0,0)),
    "z": load_img("z", (0,0,0)),
    " ": load_img("space", (0,0,0)),
    "0": load_img("0", (0,0,0)),
    "1": load_img("1", (0,0,0)),
    "2": load_img("2", (0,0,0)),
    "3": load_img("3", (0,0,0)),
    "4": load_img("4", (0,0,0)),
    "5": load_img("5", (0,0,0)),
    "6": load_img("6", (0,0,0)),
    "7": load_img("7", (0,0,0)),
    "8": load_img("8", (0,0,0)),
    "9": load_img("9", (0,0,0)),
    "/": load_img("tick", (0,0,0)),
}