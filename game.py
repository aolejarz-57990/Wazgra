import pygame
from random import randint
from gameobject.snake import Snake
from gameobject.apple import Apple
from settings import RECORD_FILE_NAME, BACKGROUND_COLOR, BLACK, MAP_SIZE


class Game:
    def __init__(self, window_size: tuple[int, int], fps: int):
        self.window_size = window_size
        self.fps = fps
        self.field_size = min(window_size) / MAP_SIZE 

        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption('Snake')
        
        self.clock = pygame.time.Clock()

        self._set_up_game()
        self.record = self._get_record()
    

    def _set_up_game(self):

        self.snake1 = Snake(3, 3)
        self.snake1.direction = 'RIGHT'

        self.snake2 = Snake(MAP_SIZE - 4, MAP_SIZE - 4)
        self.snake2.direction = 'LEFT'

        self.apple = self._spawn_apple()

    def _update_record(self, new_score):
        with open(RECORD_FILE_NAME, 'w') as f:
            f.write(str(new_score))
    
    def _get_record(self):
        with open(RECORD_FILE_NAME) as f:
            return int(f.read().strip())
            

    def _get_points(self, snake):
        return len(snake.tail)

    def _spawn_apple(self):

        x = randint(0, MAP_SIZE - 1)
        y = randint(0, MAP_SIZE - 1)

        return Apple(x, y)

    def _frame(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.apple.draw(self.screen, self.field_size)
        self.snake1.draw(self.screen, self.field_size)
        self.snake2.draw(self.screen, self.field_size)

        font = pygame.font.Font(None,30)
        if self._all_snakes_dead():
            snake1_points = self._get_points(self.snake1)
            snake2_points = self._get_points(self.snake2)

            text_surface = font.render(f"Koniec gry. Rekord: {self.record} | Gracz I: {snake1_points} | Gracz II: {snake2_points}", True, BLACK)
            text_rect = text_surface.get_rect(center=(self.window_size[0] / 2, self.window_size[1] / 2))

            self.screen.blit(text_surface, text_rect)        

        else:
            text_surface = font.render(f"GRACZ I: Ilość punktów: {self._get_points(self.snake1)}", True, BLACK)
            self.screen.blit(text_surface, (0,0))
            text_surface = font.render(f"GRACZ II: Ilość punktów: {self._get_points(self.snake2)},", True, BLACK)
            self.screen.blit(text_surface, (self.window_size[0] - text_surface.get_width(),0))

    def _all_snakes_dead(self):
        return self.snake1.dead and self.snake2.dead
    
    def _update_snake(self, snake):
        if not snake.dead:
            snake.move()
        
        if snake.collides(self.apple):
            snake.eat()
            self.apple = self._spawn_apple()

    def _update(self):
        self._update_snake(self.snake1)
        self._update_snake(self.snake2)

        if self.snake1.collides_with_tail(self.snake2):
            self.snake2.dead = True
        
        if self.snake2.collides_with_tail(self.snake1):
            self.snake1.dead = True

        if self.snake1.collides(self.snake2):
            self.snake1.dead = True 
            self.snake2.dead = True
    

        #akrualizacja rekordu przy smierci weza 
        if self._all_snakes_dead():
            snake1_points = self._get_points(self.snake1)
            snake2_points = self._get_points(self.snake2)

            points = max(snake1_points, snake2_points)

            if points > self.record:
                self.record = points
                self._update_record(points)

        
    def _handle_keyboard_input(self, key):
        #steroanie gracz I
        if key == pygame.K_w and self.snake1.direction != 'DOWN':
            self.snake1.direction = 'UP'

        elif key == pygame.K_s and self.snake1.direction != 'UP':
            self.snake1.direction = 'DOWN'

        elif key == pygame.K_a and self.snake1.direction != 'RIGHT':
            self.snake1.direction = 'LEFT'

        elif key == pygame.K_d and self.snake1.direction != 'LEFT':
            self.snake1.direction = 'RIGHT'
        
        #sterowanie graczII
        if key == pygame.K_UP and self.snake2.direction != 'DOWN':
            self.snake2.direction = 'UP'

        elif key == pygame.K_DOWN and self.snake2.direction != 'UP':
            self.snake2.direction = 'DOWN'

        elif key == pygame.K_LEFT and self.snake2.direction != 'RIGHT':
            self.snake2.direction = 'LEFT'

        elif key == pygame.K_RIGHT and self.snake2.direction != 'LEFT':
            self.snake2.direction = 'RIGHT'


        elif key == pygame.K_r and self._all_snakes_dead():
            self._set_up_game()

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