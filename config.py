import random
import pygame

# colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
FULL_WHITE = (255, 255, 255)
RED = (200, 0, 0)

# dimensions (should be divisible by BLOCKSIZE)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600
BLOCKSIZE = 20 # size of one square

FPS = 60

NEXT_MOVE_TIME = 250 # time in ms to make next move
SPEED_BTN_TXTS = ["SLOW", "MEDIUM", "FAST"]
SPEEDS = [350, 250, 150]

random.seed(None)

pygame.font.init()
game_over_font = pygame.font.SysFont('Agency FB', 60)
score_font = pygame.font.SysFont('Agency FB', 20)