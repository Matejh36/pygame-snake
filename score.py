from config import *
import pygame

class Score:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.render()

    def render(self):
        self.textsurface = score_font.render(str(self.score), True, FULL_WHITE)
        self.w, self.h = self.textsurface.get_size()
        self.blit_text()

    def blit_text(self):
        self.screen.blit(self.textsurface, (WINDOW_WIDTH - 10 - self.w, 10)) # margin top: 10, right: 10

    def clear_score(self):
        old = score_font.render(str(self.score), True, BLACK)
        w, h = old.get_size()
        rect = pygame.Rect(WINDOW_WIDTH - 10 - w, 10, w, h)
        pygame.draw.rect(self.screen, BLACK, rect, 0)

    def increase(self):
        self.clear_score()
        self.score += 1
        self.render()

    def get_score(self):
        return self.score