import pygame
from abc import ABC, abstractmethod
from typing import Self


class GameObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass
    
    def collides(self, other: Self):
        return self.x == other.x and self.y == other.y