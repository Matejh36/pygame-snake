#!/usr/bin/env python3

import pygame
import time
import sys
import random

random.seed(None)

# colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200, 0, 0)

# dimensions (should be divisible by BLOCKSIZE)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600
BLOCKSIZE = 20 # size of one square

FPS = 60

NEXT_MOVE_TIME = 250
SPEED_BTN_TXTS = ["SLOW", "MEDIUM", "FAST"]
SPEEDS = [350, 250, 150]

pygame.font.init()
myfont = pygame.font.SysFont('Agency FB', 60)
myfont2 = pygame.font.SysFont('Agency FB', 20)

class Game():
    def __init__(self):
        global SCREEN, CLOCK
        pygame.init()
        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake game')
        SCREEN.fill(BLACK)
        CLOCK = pygame.time.Clock()

    def menu(self):
        redraw = True
        speed_opt = 1

        while True:
            if redraw:
                redraw = False
                self.draw_menu(speed_opt)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    if self.btn_play.collidepoint(mouse_pos):
                        self.play()
                        redraw = True

                    for idx, btn in enumerate(self.speed_btns):
                        if btn.collidepoint(mouse_pos):
                            global NEXT_MOVE_TIME
                            NEXT_MOVE_TIME = SPEEDS[idx]
                            speed_opt = idx
                            self.draw_menu(idx)

            pygame.display.update()
            CLOCK.tick(FPS)

    def draw_menu(self, speed_opt):
        self.speed_btns = [None, None, None]

        SCREEN.fill(BLACK)
        btn_play = pygame.Rect(WINDOW_WIDTH/2 - 50, 100, 100, 40)
        pygame.draw.rect(SCREEN, WHITE, btn_play, 2)

        textsurface = myfont2.render('START', True, WHITE)
        w, h = textsurface.get_size()
        SCREEN.blit(textsurface, (btn_play.x + btn_play.width/2 - w/2, btn_play.y + btn_play.height/2 - h/2))

        btn_idxs = [0,1,2]
        btn_idxs.remove(speed_opt)

        for btn_idx in btn_idxs:
            btn = pygame.Rect(WINDOW_WIDTH/4*(btn_idx+1) - 50, 200, 100, 40)
            pygame.draw.rect(SCREEN, WHITE, btn, 2)
            btn_txt = myfont2.render(SPEED_BTN_TXTS[btn_idx], True, WHITE)
            w, h = btn_txt.get_size()
            SCREEN.blit(btn_txt, (btn.x + btn.width/2 - w/2, btn.y + btn.height/2 - h/2))
            self.speed_btns[btn_idx] = btn
        
        btn = pygame.Rect(WINDOW_WIDTH/4*(speed_opt+1) - 50, 200, 100, 40)
        pygame.draw.rect(SCREEN, WHITE, btn)
        btn_txt = myfont2.render(SPEED_BTN_TXTS[speed_opt], True, BLACK)
        w, h = btn_txt.get_size()
        SCREEN.blit(btn_txt, (btn.x + btn.width/2 - w/2, btn.y + btn.height/2 - h/2))
        self.speed_btns[speed_opt] = btn

        self.btn_play = btn_play

    def play(self):
        SCREEN.fill(BLACK)

        MOVE = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE, NEXT_MOVE_TIME)

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
            CLOCK.tick(FPS)

        textsurface = myfont.render('GAME OVER', True, (255, 255, 255))
        w, h = textsurface.get_size()
        SCREEN.blit(textsurface, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/3 - h/2))

        string = "SCORE: " + str(s.score())

        textsurface2 = myfont2.render(string, True, (255, 255, 255))
        w, h = textsurface2.get_size()
        SCREEN.blit(textsurface2, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/2 - h/2))

        pygame.display.update()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

class Snake:
    def __init__(self, fruit):
        self.body = list()
        self.actual_dir = "right"
        self.next_dir = "right"

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
            return False

        # remove last body part if no fruit to eat
        if not self.f.eat(x, y):
            pygame.draw.rect(SCREEN, BLACK, self.body[-1], 0)
            self.body.pop()
        else:
            self.f.generate(self.body)

        # draw new head position, add body part to start of the list
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect, 0)
        pygame.draw.rect(SCREEN, BLACK, rect, 1)
        self.body.insert(0, rect)

        # if no collision, return True and continue in game
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
        self.x = random.randint(0, WINDOW_WIDTH/20-1)*20
        self.y = random.randint(0, WINDOW_HEIGHT/20-1)*20

        while self.y == WINDOW_HEIGHT / 2 - ((WINDOW_HEIGHT / 2) % BLOCKSIZE) and self.x < 3:
            self.x = random.randint(0, WINDOW_WIDTH/20-1)*20
            self.y = random.randint(0, WINDOW_HEIGHT/20-1)*20

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
    g = Game()
    g.menu()

    pygame.quit()
    sys.exit()