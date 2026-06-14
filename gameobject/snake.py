from gameobject.gameobject import GameObject
import pygame
from settings import SNAKE_TAIL_COLOR, SNAKE_HEAD_COLOR, MAP_SIZE

class SnakeTailPart(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def draw(self, screen: pygame.Surface, field_size):
        screen_x = self.x * field_size
        screen_y = self.y * field_size

        pygame.draw.rect(screen, SNAKE_TAIL_COLOR, (screen_x, screen_y, field_size, field_size))


class Snake(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.direction = 'UP'
        self.dead = False

        self.tail = []

    def collides_with_tail(self, game_object):
        for tail_part in self.tail:
            if game_object.collides(tail_part):
                return True

        return False   
    
    def eat(self):
        self.tail.append(SnakeTailPart(self.x, self.y))

    def _move_head(self, prev_pos):
        

        if self.direction == 'UP':
            self.y -= 1
        elif self.direction == 'DOWN':
            self.y += 1
        elif self.direction == 'LEFT':
            self.x -= 1
        elif self.direction == 'RIGHT':
            self.x += 1

        if self.y < 0 or self.y > MAP_SIZE - 1 or \
            self.x < 0 or self.x > MAP_SIZE - 1: 

            self.dead = True
            self.x, self.y = prev_pos


    def move(self):
        prev_pos = (self.x, self.y)

        self._move_head(prev_pos)
    
        if self.dead:
            return
        
        if self.collides_with_tail(self):
            self.dead = True
            self.x, self.y = prev_pos
            return
        
        move_to_pos = prev_pos

        for tail_part in self.tail:
            prev_tail_part_pos = tail_part.x, tail_part.y
            tail_part.x, tail_part.y = move_to_pos
            move_to_pos = prev_tail_part_pos


    def draw(self, screen: pygame.Surface, field_size):
        screen_x = self.x * field_size
        screen_y = self.y * field_size

        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, (screen_x, screen_y, field_size, field_size))

        for tail_part in self.tail:
            tail_part.draw(screen)