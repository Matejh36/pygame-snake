#!/usr/bin/env python3

import pygame
import sys

from snake import Snake
from config import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake game')
        self.screen.fill(BLACK)
        self.clock = pygame.time.Clock()

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
            self.clock.tick(FPS)

    def draw_menu(self, speed_opt):
        self.speed_btns = [None, None, None]

        self.screen.fill(BLACK)
        btn_play = pygame.Rect(WINDOW_WIDTH/2 - 50, 100, 100, 40)
        pygame.draw.rect(self.screen, WHITE, btn_play, 2)

        textsurface = score_font.render('START', True, WHITE)
        w, h = textsurface.get_size()
        self.screen.blit(textsurface, (btn_play.x + btn_play.width/2 - w/2, btn_play.y + btn_play.height/2 - h/2))

        btn_idxs = [0,1,2]
        btn_idxs.remove(speed_opt)

        for btn_idx in btn_idxs:
            btn = pygame.Rect(WINDOW_WIDTH/4*(btn_idx+1) - 50, 200, 100, 40)
            pygame.draw.rect(self.screen, WHITE, btn, 2)
            btn_txt = score_font.render(SPEED_BTN_TXTS[btn_idx], True, WHITE)
            w, h = btn_txt.get_size()
            self.screen.blit(btn_txt, (btn.x + btn.width/2 - w/2, btn.y + btn.height/2 - h/2))
            self.speed_btns[btn_idx] = btn
        
        btn = pygame.Rect(WINDOW_WIDTH/4*(speed_opt+1) - 50, 200, 100, 40)
        pygame.draw.rect(self.screen, WHITE, btn)
        btn_txt = score_font.render(SPEED_BTN_TXTS[speed_opt], True, BLACK)
        w, h = btn_txt.get_size()
        self.screen.blit(btn_txt, (btn.x + btn.width/2 - w/2, btn.y + btn.height/2 - h/2))
        self.speed_btns[speed_opt] = btn

        self.btn_play = btn_play

    def play(self):
        pause = False

        self.screen.fill(BLACK)

        MOVE = pygame.USEREVENT + 1
        pygame.time.set_timer(MOVE, NEXT_MOVE_TIME)

        s = Snake(self.screen)

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

                    if event.key == pygame.K_p:
                        if pause:
                            pygame.time.set_timer(MOVE, NEXT_MOVE_TIME)
                        else:
                            pygame.time.set_timer(MOVE, 0)

                        pause = not pause

                elif event.type == MOVE:
                    if not s.move():
                        end = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if end:
                break

            pygame.display.update()
            self.clock.tick(FPS)

        textsurface = game_over_font.render('GAME OVER', True, FULL_WHITE)
        w, h = textsurface.get_size()
        self.screen.blit(textsurface, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/3 - h/2))

        string = "SCORE: " + str(s.get_score())

        textsurface2 = score_font.render(string, True, FULL_WHITE)
        w, h = textsurface2.get_size()
        self.screen.blit(textsurface2, (WINDOW_WIDTH/2 - w/2, WINDOW_HEIGHT/2 - h/2))

        pygame.display.update()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
 
if __name__ == "__main__":
    g = Game()
    g.menu()

    pygame.quit()
    sys.exit()