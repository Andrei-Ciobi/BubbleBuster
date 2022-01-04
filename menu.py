import pygame.sprite
from Utyls.variables import *
from components import Button

class Menu(pygame.sprite.Sprite):
    def __init__(self, color, screen, x, y, text1, text2):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
        self.rect.centerx = x
        self.rect.centery = y
        self.color = color
        self.screen = screen
        self.buttons = []
        self.render1 = self.getText(text1)
        self.textRect1 = self.render1.get_rect()
        self.textRect1.centerx = self.rect.centerx
        self.textRect1.centery = self.rect.centery - 120
        self.render2 = self.getText(text2)
        self.textRect2 = self.render2.get_rect()
        self.textRect2.centerx = self.rect.centerx
        self.textRect2.centery = self.rect.centery - 80

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.render1, self.textRect1)
        self.screen.blit(self.render2, self.textRect2)
        for button in self.buttons:
            if isinstance(button, Button):
                button.draw()

    def getText(self, text1):
        myFont = pygame.font.SysFont(FONT_STYLE, BUTTON_FONT_SIZE)
        return myFont.render(text1, True, COLOR_WHITE, COLOR_NAVYBLUE)

    def updateScoreText(self, text2):
        self.render2 = self.getText(text2)