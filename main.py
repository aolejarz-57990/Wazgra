import pygame

from game import Game

WINDOW_SIZE = (800, 800)
FPS = 4

pygame.init()

if __name__ == '__main__':
    game = Game(WINDOW_SIZE, FPS)
    game.start_loop()

    pygame.quit()