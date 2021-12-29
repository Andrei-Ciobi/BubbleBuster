import random

import pygame.font
from Utyls.variables import *
from components import Bubble, Score, ShootingPoint
from table import Table
import numpy as np

class BubbleGame(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Width, height
        self.table = Table(self.screen)
        self.score = Score(self.screen)
        self.shootingPoint = ShootingPoint()
        self.clock = pygame.time.Clock()
        self.shootingBubble = None
        self.nextShootingBubble = None
        self.running = False
        self.endGame = False

    # Loads the level
    def loadLevel(self, level):
        self.table.loadLevel("Levels/" + str(level) + ".txt")

    # Loads the bubble that will be shooted
    def loadShootingBubble(self):
        self.shootingBubble = self.nextShootingBubble  # self.nextShootingBubble
        self.shootingBubble.rect.centerx = self.shootingPoint.positionX
        self.shootingBubble.rect.centery = self.shootingPoint.positionY

    # Loads the bubble that will be shooted after the curent bubble is shoot
    def loadNextShootingBubble(self):
        nArray = np.array(self.table.colorsUsed)
        indexes = np.where(nArray != 0)[0].tolist()

        if len(indexes) != 0:
            colorUsed = random.choice(indexes)
        else:
            colorUsed = COLOR_VECTOR.index(COLOR_BLACK)

        self.nextShootingBubble = Bubble(COLOR_VECTOR[colorUsed], self.screen, 0, 0)
        self.nextShootingBubble.rect.centerx = self.shootingPoint.positionX + 200
        self.nextShootingBubble.rect.centery = self.shootingPoint.positionY

    # Checks and deletes the floating bubbles
    def checkAndDeleteFloaters(self):

        connectedBubbles = self.table.getConnectedBubbles()

        if connectedBubbles != 0:
            self.table.deleteFloatingBubbles(connectedBubbles)
        else:
            self.table.deleteFloatingBubbles(self.table.bubbleList)
            self.endGame = True

    # Draws the components on the screen
    def draw(self):
        self.screen.fill(COLOR_BLACK)
        self.table.draw()
        self.shootingBubble.draw()
        self.nextShootingBubble.draw()
        self.score.draw()

    def run(self):
        self.loadLevel("level3")
        self.loadNextShootingBubble()
        self.loadShootingBubble()
        self.loadNextShootingBubble()

        self.running = True
        shooting = False

        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP and not shooting:
                    self.shootingPoint.update()
                    self.shootingBubble.shootingAngle = self.shootingPoint.angle
                    shooting = True

            # If we pressed click to shoot
            if shooting == True:
                self.shootingBubble.update()

                # Check if we hit something
                succes = self.table.checkForCollision(self.shootingBubble)

                # If we didn't hit something we check for top collision
                if succes == False:
                    succes = self.table.checkForTopCollision(self.shootingBubble)

                # If we hit a bubble on the matrix we check if we can delete a sequece
                if succes != False:

                    # print(self.table.colorsUsed)

                    # Get the connected bubbles
                    response, resultList = self.table.getDeletedBubbles()

                    # If 3+ connected we delete them and update the score
                    if response == True:
                        scoreResult = self.table.deleteBubbles(resultList)
                        self.score.update(scoreResult)

                        # Checks if there are floating bubbles and deletes them
                        self.checkAndDeleteFloaters()

                    # Generate new shooting bubble
                    self.loadShootingBubble()
                    self.loadNextShootingBubble()

                    # We no longer shoot
                    shooting = False
                    # print(self.table.colorsUsed)

            # update the window every 60 FPS
            pygame.display.update()
            self.clock.tick(120)
