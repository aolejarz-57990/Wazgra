from gameobject.gameobject import GameObject
import pygame
from settings import APPLE_COLOR

class Apple(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen: pygame.Surface, field_size):
        screen_x = self.x * field_size
        screen_y = self.y * field_size

        pygame.draw.rect(screen, APPLE_COLOR, (screen_x, screen_y, field_size, field_size))