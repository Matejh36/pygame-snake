#!/usr/bin/env python3

import pygame
import time
import sys
import random

random.seed(None)

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600
BLOCKSIZE = 20

pygame.font.init()
myfont = pygame.font.SysFont('Agency FB', 60)
myfont2 = pygame.font.SysFont('Agency FB', 20)

def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(BLACK)

    CLOCK = pygame.time.Clock()
    MOVE = pygame.USEREVENT + 1
    pygame.time.set_timer(MOVE, 350)

    f = Fruit()
    s = Snake(f)

    end = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    s.set_direction("left")
                if event.key == pygame.K_RIGHT:
                    s.set_direction("right")
                if event.key == pygame.K_UP:
                    s.set_direction("up")
                if event.key == pygame.K_DOWN:
                    s.set_direction("down")
            elif event.type == MOVE:
                if not s.move():
                    end = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if end:
            break

        pygame.display.update()
        CLOCK.tick(30)

    textsurface = myfont.render('GAME OVER', False, (255, 255, 255))
    w, h = myfont.size("GAME OVER")
    SCREEN.blit(textsurface, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/3 - h/2))

    string = "SCORE: " + str(s.score())

    textsurface2 = myfont2.render(string, False, (255, 255, 255))
    w, h = myfont2.size(string)
    SCREEN.blit(textsurface2, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/2 - h/2))

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            break

class Snake:
    body = list()
    direction = "right"

    def __init__(self, fruit):
        self.f = fruit
        x = 0
        y = WINDOW_HEIGHT / 2 - ((WINDOW_HEIGHT / 2) % BLOCKSIZE)

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
        self.body.append(rect)

        x = x + BLOCKSIZE

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
        self.body.insert(0, rect)

        x = x + BLOCKSIZE

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
        self.body.insert(0, rect)

    def set_direction(self, dir):
        self.direction = dir

    def move(self):
        x = self.body[0].x
        y = self.body[0].y

        if self.direction == "up":
            y = y - BLOCKSIZE
        elif self.direction == "down":
            y = y + BLOCKSIZE
        elif self.direction == "left":
            x = x - BLOCKSIZE
        elif self.direction == "right":
            x = x + BLOCKSIZE

        if self.check_collision(x, y):
            return False

        if not self.f.eat(x, y):
            pygame.draw.rect(SCREEN, BLACK, self.body[-1], 0)
            self.body.pop()
        else:
            self.f.generate(self.body)

        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
        self.body.insert(0, rect)

        return True

    def check_collision(self, x, y):
        if x < 0 or y < 0 or x > WINDOW_WIDTH - BLOCKSIZE or y > WINDOW_HEIGHT - BLOCKSIZE:
            return True

        for body_part in self.body:
            if x == body_part.x and y == body_part.y:
                return True

        return False

    def score(self):
        return len(self.body) - 3

class Fruit:
    x = 0
    y = 0

    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH/20)*20
        self.y = random.randint(0, WINDOW_HEIGHT/20)*20

        while self.y == WINDOW_HEIGHT / 2 - ((WINDOW_HEIGHT / 2) % BLOCKSIZE) and self.x < 3:
            self.x = random.randint(0, WINDOW_WIDTH/20)*20
            self.y = random.randint(0, WINDOW_HEIGHT/20)*20

        rect = pygame.Rect(self.x, self.y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, RED, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)

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
        pygame.draw.rect(SCREEN, RED, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
 

if __name__ == "__main__":
    main()