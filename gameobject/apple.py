from gameobject.gameobject import GameObject
import pygame
from settings import FIELD_SIZE, APPLE_COLOR

class Apple(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen: pygame.Surface):
        screen_x = self.x * FIELD_SIZE
        screen_y = self.y * FIELD_SIZE

        pygame.draw.rect(screen, APPLE_COLOR, (screen_x, screen_y, FIELD_SIZE, FIELD_SIZE))