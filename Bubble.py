import pygame.sprite
import pygame.gfxdraw
from Utyls.variables import *


class Bubble(pygame.sprite.Sprite):
    def __init__(self, color, screen, row, column):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, REC_WIDTH, REC_HEIGHT)
        self.rect.centerx = int(column * SPACE_WIDTH + REC_WIDTH / 2) + 3
        self.rect.centery = int(row * (REC_HEIGHT + 2) + REC_HEIGHT / 2)
        self.color = color
        self.radius = int(REC_WIDTH / 2) + 2
        self.screen = screen
        if row % 2 != 0:
            self.rect.centerx += int(REC_WIDTH / 2) + 5

    def draw(self):
        # pygame.draw.rect(self.screen, WHITE, self.rect)
        pygame.gfxdraw.filled_circle(self.screen, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(self.screen, self.rect.centerx, self.rect.centery, self.radius, GRAY)

    def __str__(self):
        return str(self.rect.centerx) + " " + str(self.rect.centery)
