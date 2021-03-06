import math

import pygame.sprite
import pygame.gfxdraw
from Utyls.variables import *


class Bubble(pygame.sprite.Sprite):
    def __init__(self, color, screen, row, column):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(0, 0, REC_WIDTH, REC_HEIGHT)
        self.rect.centerx = int(column * SPACE_WIDTH + REC_WIDTH / 2) + 3
        self.rect.centery = int(row * (REC_HEIGHT + 2) + REC_HEIGHT / 2)
        self.x = 0
        self.y = 0
        self.color = color
        self.radius = int(REC_WIDTH / 2) + 2
        self.screen = screen
        self.row = row
        self.column = column
        self.shootingAngle = 90
        if row % 2 != 0:
            self.rect.centerx += int(REC_WIDTH / 2) + 5

    def draw(self):
        pygame.gfxdraw.filled_circle(self.screen, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(self.screen, self.rect.centerx, self.rect.centery, self.radius, COLOR_GRAY)

    def update(self):
        if self.rect.right >= SCREEN_WIDTH - 10:
            self.shootingAngle = 180 - self.shootingAngle
        elif self.rect.left <= 10:
            self.shootingAngle = 180 - self.shootingAngle

        if self.shootingAngle == 90:
            x = 0
            y = BUBBLE_SPEED * -1
        elif self.shootingAngle < 90:
            x, y = self.calculateMovement(180 - self.shootingAngle)
        elif self.shootingAngle > 90:
            x, y = self.calculateMovement(self.shootingAngle)
            x *= -1

        self.x += x
        self.y += y

        self.rect.x = self.x
        self.rect.y = self.y

    def updateValues(self, row, column):
        self.row = row
        self.column = column
        if self.row % 2 != 0 and self.column == COLUMNS - 1:
            self.column -= 1

        print(self.row, " ", self.column)

        self.rect.centerx = int(self.column * SPACE_WIDTH + REC_WIDTH / 2) + 3
        self.rect.centery = int(self.row * (REC_HEIGHT + 2) + REC_HEIGHT / 2)
        if self.row % 2 != 0:
            self.rect.centerx += int(REC_WIDTH / 2) + 5

    @staticmethod
    def calculateMovement(angle):
        rad = math.radians(angle)

        x = math.cos(rad) * BUBBLE_SPEED
        y = math.sin(rad) * BUBBLE_SPEED * -1

        return x, y

    def __str__(self):
        return str(self.rect.centerx) + " " + str(self.rect.centery)


# Score component

class Score(object):
    def __init__(self, screen):
        self.screen = screen
        self.totalScore = 0
        self.render = self.updateTotalScoreValue(self.totalScore)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = SCREEN_HEIGHT - 5

    # Draws the score on the screen
    def draw(self):
        self.screen.blit(self.render, self.rect)

    # Updates the score, must be changed to recive a list of all the popped bubbles and calculate the score with them
    def update(self, score):
        self.totalScore += score
        self.render = self.updateTotalScoreValue(self.totalScore)

    def initiateScore(self):
        self.totalScore = 0
        self.render = self.updateTotalScoreValue(self.totalScore)

    @staticmethod
    def updateTotalScoreValue(value):
        myFont = pygame.font.SysFont(FONT_STYLE, FONT_SIZE)
        return myFont.render('Total score ' + str(value), True, COLOR_WHITE, COLOR_BLACK)


# Shooting cannon

class ShootingPoint(object):
    def __init__(self):
        self.positionX = round(SCREEN_WIDTH / 2)
        self.positionY = SCREEN_HEIGHT - 50
        self.angle = 0

    def update(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        dx = (mouseX - self.positionX)
        dy = (mouseY - self.positionY)

        rads = math.atan2(dy, dx)
        rads %= 2 * math.pi

        self.angle = math.degrees(rads) - 180
        print(self.angle)

        if self.angle >= 175 or self.angle <= -170:
            self.angle = 175
        elif self.angle <= 5 and self.angle >= -10:
            self.angle = 5
        elif self.angle < -10 and self.angle > -170:
            self.angle = 90

class Button(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, color, text, type):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.rect.centerx = x
        self.rect.centery = y
        self.color = color
        self.screen = screen
        self.clicked = False
        self.render = self.getText(text)
        self.textRect = self.render.get_rect()
        self.textRect.centerx = self.rect.centerx
        self.textRect.centery = self.rect.centery
        self.type = type

    def draw(self):
        pygame.draw.rect(self.screen, COLOR_WHITE, self.rect)
        self.screen.blit(self.render, self.textRect)

    def pressed(self):
        action = False
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        return action, self.type


    def getText(self, text):
        myFont = pygame.font.SysFont(FONT_STYLE, BUTTON_FONT_SIZE)
        return myFont.render(text, True, COLOR_BLACK, COLOR_WHITE)