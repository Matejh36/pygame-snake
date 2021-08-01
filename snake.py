from score import Score
from fruit import Fruit
from config import *
import pygame

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.body = list()
        self.actual_dir = "right"
        self.next_dir = "right"

        x = 0
        y = WINDOW_HEIGHT / 2 - ((WINDOW_HEIGHT / 2) % BLOCKSIZE)

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 0)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        self.body.append(rect)

        x = x + BLOCKSIZE

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 0)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        self.body.insert(0, rect)

        x = x + BLOCKSIZE

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 0)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        self.body.insert(0, rect)

        self.f = Fruit(self.screen, self.body)
        self.score = Score(self.screen)

    def set_direction(self, dir):
        # 180° turn check
        if self.actual_dir == "left" and dir == "right" or self.actual_dir == "right" and dir == "left" or self.actual_dir == "up" and dir == "down" or self.actual_dir == "down" and dir == "up":
            return

        self.next_dir = dir

    def move(self):
        # change direction
        self.actual_dir = self.next_dir

        # get head position
        x = self.body[0].x
        y = self.body[0].y

        # calculate new head position
        if self.actual_dir == "up":
            y = y - BLOCKSIZE
        elif self.actual_dir == "down":
            y = y + BLOCKSIZE
        elif self.actual_dir == "left":
            x = x - BLOCKSIZE
        elif self.actual_dir == "right":
            x = x + BLOCKSIZE

        # if collision, return False, end game
        if self.check_collision(x, y):
            self.score.clear_score()
            return False

        # remove last body part if no fruit to eat
        if not self.f.eat(x, y):
            pygame.draw.rect(self.screen, BLACK, self.body[-1], 0)
            self.body.pop()
        else:
            self.f.generate(self.body)
            self.score.increase()

        # draw new head position, add body part to start of the list
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(self.screen, WHITE, rect, 0)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        self.body.insert(0, rect)

        self.score.blit_text()

        # if no collision, return True and continue in game
        return True

    def check_collision(self, x, y):
        if x < 0 or y < 0 or x > WINDOW_WIDTH - BLOCKSIZE or y > WINDOW_HEIGHT - BLOCKSIZE:
            return True

        for body_part in self.body:
            if x == body_part.x and y == body_part.y:
                return True

        return False

    def get_score(self):
        return self.score.get_score()