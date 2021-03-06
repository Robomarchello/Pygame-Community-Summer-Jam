
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

grassy_right = pygame.image.load("assets/images/grassy_caves/right.png").convert()
grassy_right.set_colorkey((255, 255, 255))
grassy_left = pygame.image.load("assets/images/grassy_caves/left.png").convert()
grassy_left.set_colorkey((255, 255, 255))

grassy_side_left = pygame.image.load("assets/images/grassy_caves/side_left.png").convert()
grassy_side_left.set_colorkey((255, 255, 255))
grassy_side_right = pygame.image.load("assets/images/grassy_caves/side_right.png").convert()
grassy_side_right.set_colorkey((255, 255, 255))

dungeon_top = pygame.image.load("assets/images/dungeon_cave/top.png").convert()
dungeon_top.set_colorkey((255, 255, 255))
dungeon_right = pygame.image.load("assets/images/dungeon_cave/right.png").convert()
dungeon_right.set_colorkey((255, 255, 255))
dungeon_left = pygame.image.load("assets/images/dungeon_cave/left.png").convert()
dungeon_left.set_colorkey((255, 255, 255))
dungeon_side_left = pygame.image.load("assets/images/dungeon_cave/side_left.png").convert()
dungeon_side_left.set_colorkey((255, 255, 255))
dungeon_side_right = pygame.image.load("assets/images/dungeon_cave/side_right.png").convert()
dungeon_side_right.set_colorkey((255, 255, 255))
dungeon_base = pygame.image.load("assets/images/dungeon_cave/base.png").convert()
dungeon_base.set_colorkey((255, 255, 255))

lava_top = pygame.image.load("assets/images/lava_cave/top.png").convert()
lava_top.set_colorkey((255, 255, 255))
lava_right = pygame.image.load("assets/images/lava_cave/right.png").convert()
lava_right.set_colorkey((255, 255, 255))
lava_left = pygame.image.load("assets/images/lava_cave/left.png").convert()
lava_left.set_colorkey((255, 255, 255))
lava_side_left = pygame.image.load("assets/images/lava_cave/side_left.png").convert()
lava_side_left.set_colorkey((255, 255, 255))
lava_side_right = pygame.image.load("assets/images/lava_cave/side_right.png").convert()
lava_side_right.set_colorkey((255, 255, 255))
lava_base = pygame.image.load("assets/images/lava_cave/base.png").convert()
lava_base.set_colorkey((255, 255, 255))

green_top = pygame.image.load("assets/images/green_cave/top.png").convert()
green_top.set_colorkey((255, 255, 255))
green_right = pygame.image.load("assets/images/green_cave/right.png").convert()
green_right.set_colorkey((255, 255, 255))
green_left = pygame.image.load("assets/images/green_cave/left.png").convert()
green_left.set_colorkey((255, 255, 255))
green_side_left = pygame.image.load("assets/images/green_cave/side_left.png").convert()
green_side_left.set_colorkey((255, 255, 255))
green_side_right = pygame.image.load("assets/images/green_cave/side_right.png").convert()
green_side_right.set_colorkey((255, 255, 255))
green_base = pygame.image.load("assets/images/green_cave/base.png").convert()
green_base.set_colorkey((255, 255, 255))


chain_img = pygame.image.load("assets/images/dungeon_cave/chain.png").convert()
chain_img.set_colorkey((255, 255, 255))

skeleton_hit_img = pygame.image.load("assets/images/dungeon_cave/skeleton_hit.png").convert()
skeleton_hit_img.set_colorkey((255, 255, 255))

cursor_img = pygame.image.load("assets/images/cursor.png").convert()
cursor_img.set_colorkey((0, 0, 0))

worm_walk_imgs = [load_img("worm_walk1", base="images"), load_img("worm_walk2", base="images"), load_img("worm_walk3", base="images")]
worm_hit_img = load_img("worm_hit", base="images")

fly_hit_img = load_img("fly_hit", base="images")

lava_imgs = [load_img("lava1", base="images/lava_cave"), load_img("lava2", base="images/lava_cave"),
load_img("lava3", base="images/lava_cave"), load_img("lava4", base="images/lava_cave")]

LavaCrabImg = pygame.image.load('assets/images/lava_cave/LavaCrab.png').convert()
LavaCrabHit = pygame.image.load('assets/images/lava_cave/LavaCrabHit.png').convert()

MagicOrbImage = pygame.image.load('assets/images/lava_cave/MagicOrbImg.png').convert()
MagicOrbImage.set_colorkey((255, 255, 255))
MagicOrbHit = pygame.image.load('assets/images/lava_cave/MagicOrbHit.png').convert()
MagicOrbHit.set_colorkey((255, 255, 255))

bat_hit_img = load_img("green_cave/bat_hit", base="images")

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