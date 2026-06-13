from gameobject.gameobject import GameObject
import pygame
from settings import FIELD_SIZE, SNAKE_TAIL_COLOR, SNAKE_HEAD_COLOR 

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

    def collides_with_tail(self, game_object):
        for tail_part in self.tail:
            if game_object.collides(tail_part):
                return True

        return False   
    
    def eat(self):
        self.tail.append(SnakeTailPart(self.x, self.y))

    def _move_head(self, prev_pos, map_size):
        map_width, map_height = map_size
        #sterowanie Gracz I
        if self.direction == 'UP':
            self.y -= 1
        elif self.direction == 'DOWN':
            self.y += 1
        elif self.direction == 'LEFT':
            self.x -= 1
        elif self.direction == 'RIGHT':
            self.x += 1
        #sterowanie Gracz II


        # Sterowanie GRACZ II - strzałki
        elif key == pygame.K_UP and self.snake2.direction != 'DOWN':
            self.snake2.direction = 'UP'

        elif key == pygame.K_DOWN and self.snake2.direction != 'UP':
            self.snake2.direction = 'DOWN'

        elif key == pygame.K_LEFT and self.snake2.direction != 'RIGHT':
            self.snake2.direction = 'LEFT'

        elif key == pygame.K_RIGHT and self.snake2.direction != 'LEFT':
            self.snake2.direction = 'RIGHT'

        #restart gry
        elif key == pygame.K_r and self._all_snakes_dead():
            self._set_up_game()

        if self.y < 0 or self.y > map_height - 1 or \
            self.x < 0 or self.x > map_width - 1: 

            self.dead = True
            self.x, self.y = prev_pos


    def move(self, map_size):
        prev_pos = (self.x, self.y)

        self._move_head(prev_pos, map_size)
    
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


    def draw(self, screen: pygame.Surface):
        screen_x = self.x * FIELD_SIZE
        screen_y = self.y * FIELD_SIZE

        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, (screen_x, screen_y, FIELD_SIZE, FIELD_SIZE))

        for tail_part in self.tail:
            tail_part.draw(screen)