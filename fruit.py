import random
import pygame

from config import *

class Fruit:
    x = 0
    y = 0

    def __init__(self, screen, snake_pos):
        self.screen = screen
        self.generate(snake_pos)

    def eat(self, s_x, s_y):
        return self.x == s_x and self.y == s_y

    def generate(self, snake_pos):
        done = False

        while not done:
            done = True
            
            self.x = random.randint(0, (WINDOW_WIDTH/20)-1)*20
            self.y = random.randint(0, (WINDOW_HEIGHT/20)-1)*20

            for pos in snake_pos:
                if pos.x == self.x and pos.y == self.y:
                    done = False
                    break

        rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, RED, rect, 0)
        pygame.draw.rect(self.screen, BLACK, rect, 1)