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
        self.color = color
        self.radius = int(REC_WIDTH / 2) + 2
        self.screen = screen
        self.row = row
        self.column = column
        self.shootingAngle = 90
        if row % 2 != 0:
            self.rect.centerx += int(REC_WIDTH / 2) + 5

    def draw(self):
        # pygame.draw.rect(self.screen, COLOR_WHITE, self.rect)
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

        self.rect.x += x
        self.rect.y += y

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

    # def checkForColLision(self, bubbleList):
    #
    #     hits = self.rect.collidelist(bubbleList)
    #     row, column, hit = 0, 0, None
    #
    #     if hits != -1:
    #         hit = bubbleList[hits]
    #         print(hit.row, " ", hit.column)
    #         print("stanga : ", abs(self.rect.left - hit.rect.right))
    #         print("dreapta : ", abs(self.rect.right - hit.rect.left))
    #         print("jos : ", abs(self.rect.top - hit.rect.bottom))
    #         # Check for the hitted side
    #         if 0 <= abs(self.rect.top - hit.rect.bottom) <= 15:
    #             print("jos")
    #             row = 1
    #         if 0 <= abs(self.rect.left - hit.rect.right) <= 15:
    #             print("stanga")
    #             column = 1 if row == 0 else 0
    #         if 0 <= abs(self.rect.right - hit.rect.left) <= 15:
    #             print("dreapta")
    #             column = -1
    #
    #         self.row = hit.row + row
    #         self.column = hit.column + column
    #         if self.row % 2 != 0 and self.column == COLUMNS - 1:
    #             self.column -= 1
    #
    #         print(self.row, " ", self.column)
    #
    #         self.rect.centerx = int(self.column * SPACE_WIDTH + REC_WIDTH / 2) + 3
    #         self.rect.centery = int(self.row * (REC_HEIGHT + 2) + REC_HEIGHT / 2)
    #         if self.row % 2 != 0:
    #             self.rect.centerx += int(REC_WIDTH / 2) + 5
    #
    #     return hit

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
    def update(self):
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
