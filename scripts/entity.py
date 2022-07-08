import pygame
import abc

from scripts.vector2 import Vector2

class Entity(abc.ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_centered_position(self) -> pygame.Rect:
        """
        Returns the center of the entities rect
        """

        return self.rect.center

    def move_towards(self, x_pos: int, y_pos: int, speed:int) -> None:
        """
        Moves entity toward a give position
        """

        position_vector = Vector2(*self.get_centered_position())
        update_position = position_vector.move_towards(x_pos, y_pos, speed)

        return update_position

    def rot_center(self, image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

    def load_image(self, path):
        image = pygame.image.load(f"assets/images/{path}.png").convert()
        image.set_colorkey((255, 255, 255))
        return image

    def animate(self, image_list, animation_index, time_to_show_image_on_screen):
        if animation_index+1 >= len(image_list)*time_to_show_image_on_screen:
            animation_index = 0
        animation_index += 1

        return animation_index

    abc.abstractclassmethod
    def draw(self, display):
        pass