import random

import pygame.font
from Utyls.variables import *
from components import Bubble, Score, ShootingPoint, Button
from table import Table
from menu import Menu
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
        self.shooting = False
        self.win = False
        self.blockInput = False
        self.winMenu = self.initializeWinMenu()
        self.loseMenu = self.initializeLoseMenu()
        self.curentLevel = 1

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
            scoreResult = self.table.deleteFloatingBubbles(connectedBubbles)
            self.score.update(scoreResult)
        else:
            self.table.deleteFloatingBubbles(self.table.bubbleList)
            self.endGame = True

    # Draws the components on the screen
    def drawGame(self):
        self.screen.fill(COLOR_BLACK)
        self.table.draw()
        self.shootingBubble.draw()
        self.nextShootingBubble.draw()
        self.score.draw()

    def runGame(self):
        self.drawGame()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP and not self.shooting and not self.blockInput:
                self.shootingPoint.update()
                self.shootingBubble.shootingAngle = self.shootingPoint.angle
                self.shooting = True

            if self.blockInput:
                self.blockInput = False

        # If we pressed click to shoot
        if self.shooting == True:
            self.shootingBubble.update()

            # Check if we hit something
            succes = self.table.checkForCollision(self.shootingBubble)

            # Check for lose state
            if self.table.lose:
                self.endGame = True
                self.win = False
                loseText = "With " + str(self.score.totalScore) + " points"
                self.loseMenu.updateScoreText(loseText)

            # If we didn't hit something we check for top collision
            if succes == False and not self.endGame:
                succes = self.table.checkForTopCollision(self.shootingBubble)

            # If we hit a bubble on the matrix we check if we can delete a sequece
            if succes != False:

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
                self.shooting = False

                # Check if we win the game
                if len(self.table.bubbleList) == 0:
                    self.endGame = True
                    self.win = True
                    self.drawGame()
                    winText = "With " + str(self.score.totalScore) + " points"
                    self.winMenu.updateScoreText(winText)

    # Runs the end game menu
    def runEndGameMenu(self):
        # Menu for win endgame
        if self.win:
            self.winMenu.draw()
            for button in self.winMenu.buttons:
                action, buttonType = button.pressed()

                if action:
                    # Quit button
                    if buttonType == TYPE_QUIT:
                        self.running = False

                    # Next level button
                    if buttonType == TYPE_NEXT:
                        print("got in")
                        self.curentLevel = self.curentLevel + 1 if self.curentLevel < MAX_LEVELS else 1
                        self.win = False
                        self.endGame = False
                        self.blockInput = True
                        self.initiateLevel("level" + str(self.curentLevel))


        else:
            self.loseMenu.draw()

            for button in self.loseMenu.buttons:
                action, buttonType = button.pressed()

                if action:
                    # Quit button
                    if buttonType == TYPE_QUIT:
                        self.running = False

                    # Replay the curent level button
                    if buttonType == TYPE_REPLAY:
                        self.win = False
                        self.endGame = False
                        self.blockInput = True
                        self.initiateLevel("level" + str(self.curentLevel))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def initiateLevel(self, level):
        self.loadLevel(level)
        self.loadNextShootingBubble()
        self.loadShootingBubble()
        self.loadNextShootingBubble()
        self.score.initiateScore()

    def run(self):
        self.initiateLevel("level" + str(self.curentLevel))

        self.running = True

        while self.running:
            if not self.endGame:
                self.runGame()
            else:
                self.runEndGameMenu()

            # update the window every 60 FPS
            pygame.display.update()
            self.clock.tick(120)

    # Creates the menu for the win ending
    def initializeWinMenu(self):
        winText = "With " + str(self.score.totalScore) + " points"
        menu = Menu(COLOR_NAVYBLUE, self.screen, int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), "YOU WIN", winText)

        posX = menu.rect.left + BUTTON_WIDTH / 2 + 10
        posY = menu.rect.bottom - BUTTON_HEIGHT / 2 - 10
        button = Button(self.screen, posX, posY, COLOR_WHITE, "Quit", TYPE_QUIT)
        menu.buttons.append(button)

        posX = menu.rect.right - BUTTON_WIDTH / 2 - 10
        posY = menu.rect.bottom - BUTTON_HEIGHT / 2 - 10

        button = Button(self.screen, posX, posY, COLOR_WHITE, "Next", TYPE_NEXT)
        menu.buttons.append(button)

        return menu

    # Creates the menu for the lose ending
    def initializeLoseMenu(self):
        loseText = "With " + str(self.score.totalScore) + " points"
        menu = Menu(COLOR_NAVYBLUE, self.screen, int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), "YOU LOSE", loseText)

        posX = menu.rect.left + BUTTON_WIDTH / 2 + 5
        posY = menu.rect.bottom - BUTTON_HEIGHT / 2 - 5
        button = Button(self.screen, posX, posY, COLOR_WHITE, "Quit", TYPE_QUIT)
        menu.buttons.append(button)

        posX = menu.rect.right - BUTTON_WIDTH / 2 - 5
        posY = menu.rect.bottom - BUTTON_HEIGHT / 2 - 5

        button = Button(self.screen, posX, posY, COLOR_WHITE, "Replay", TYPE_REPLAY)
        menu.buttons.append(button)

        return menu
