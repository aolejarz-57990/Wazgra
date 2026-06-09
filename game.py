import pygame

from abc import ABC, abstractmethod
from random import randint

from typing import Self

BACKGROUND_COLOR = 'pink'
SNAKE_HEAD_COLOR = (0, 200, 0)
SNAKE_TAIL_COLOR = (0, 255, 0)
APPLE_COLOR = (200, 0, 0)

FIELD_SIZE = 50

class GameObject(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

    def collides(self, other: Self):
        return self.x == other.x and self.y == other.y
    

class Apple(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, screen: pygame.Surface):
        screen_x = self.x * FIELD_SIZE
        screen_y = self.y * FIELD_SIZE

        pygame.draw.rect(screen, APPLE_COLOR, (screen_x, screen_y, FIELD_SIZE, FIELD_SIZE))


class SnakeTailPart(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
    
    def draw(self, screen: pygame.Surface):
        screen_x = self.x * FIELD_SIZE
        screen_y = self.y * FIELD_SIZE

        pygame.draw.rect(screen, SNAKE_TAIL_COLOR, (screen_x, screen_y, FIELD_SIZE, FIELD_SIZE))


class Snake(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.direction = 'UP'
        self.dead = False

        self.tail = []

    def eat(self):
        self.tail.append(SnakeTailPart(self.x, self.y))

    def _move_head(self, prev_pos, map_size):
        map_width, map_height = map_size

        if self.direction == 'UP':
            self.y -= 1
        elif self.direction == 'DOWN':
            self.y += 1
        elif self.direction == 'LEFT':
            self.x -= 1
        elif self.direction == 'RIGHT':
            self.x += 1

        if self.y < 0 or self.y > map_height - 1 or \
            self.x < 0 or self.x > map_width - 1: 

            self.dead = True
            self.x, self.y = prev_pos


    def move(self, map_size):
        prev_pos = (self.x, self.y)

        self._move_head(prev_pos, map_size)
    
        if self.dead:
            return
        
        move_to_pos = prev_pos

        for tail_part in self.tail:
            prev_tail_part_pos = tail_part.x, tail_part.y
            tail_part.x, tail_part.y = move_to_pos
            move_to_pos = prev_tail_part_pos


    def draw(self, screen: pygame.Surface):
        screen_x = self.x * FIELD_SIZE
        screen_y = self.y * FIELD_SIZE

        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, (screen_x, screen_y, FIELD_SIZE, FIELD_SIZE))

        for tail_part in self.tail:
            tail_part.draw(screen)


class Game:
    def __init__(self, window_size: tuple[int, int], fps: int):
        self.window_size = window_size
        self.fps = fps

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Snake')
        
        self.clock = pygame.time.Clock()

        map_width, map_height = self._get_map_size()

        self.snake = Snake(
            map_width / 2,
            map_height / 2
        )

        self.apple = self._spawn_apple()

        self.game_over = False
        
    def _get_map_size(self):
        return (
            int(self.window_size[0] / FIELD_SIZE),
            int(self.window_size[1] / FIELD_SIZE)
        )

    def _spawn_apple(self):
        map_width, map_height = self._get_map_size()

        x = randint(0, map_width - 1)
        y = randint(0, map_height - 1)

        return Apple(x, y)

    def _frame(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.apple.draw(self.screen)
        self.snake.draw(self.screen)

    def _update(self):
        self.snake.move(self._get_map_size())

        if self.snake.collides(self.apple):
            self.snake.eat()
            self.apple = self._spawn_apple()

    def _handle_keyboard_input(self, key):
        if key == pygame.K_w:
            self.snake.direction = 'UP'
        elif key == pygame.K_s:
            self.snake.direction = 'DOWN'
        elif key == pygame.K_a:
            self.snake.direction = 'LEFT'
        elif key == pygame.K_d:
            self.snake.direction = 'RIGHT'

    def start_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.KEYDOWN:
                    self._handle_keyboard_input(event.key)
                            
            self._update()
            self._frame()

            pygame.display.flip()

            self.clock.tick(self.fps)