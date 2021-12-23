import random

import pygame.font
from Utyls.variables import *
from components import Bubble, Score, ShootingPoint
import numpy as np


# Table component
class Table(object):
    def __init__(self, screen):
        self.screen = screen
        self.matrix = self.initMatrix()
        self.bubbleList = []
        self.colorsUsed = [0 for i in range(COLUMNS)]

    # Initiate the matrix to a null matrix
    def initMatrix(self):
        return [[None for i in range(COLUMNS if j % 2 == 0 else COLUMNS - 1)] for j in range(ROWS)]
        # return [[Bubble(screen=self.screen, color=COLOR_BROWN, row=j, column=i) for i in
        #          range(COLUMNS if j % 2 == 0 else COLUMNS - 1)] for j in range(ROWS)]

    # Draw the table components
    def draw(self):
        # Draw the matrix
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                if self.matrix[row][column] != None:
                    self.matrix[row][column].draw()
            row += 1

    # Loads a predef level into the self.matrix atribute
    def loadLevel(self, fileName):
        # Load the level
        file = open(fileName, 'r')
        level = [[int(num) for num in line.split()] for line in file]

        # Update to the curent level
        row = 0
        for line in level:
            for column in range(len(line)):
                self.matrix[row][column] = \
                    Bubble(color=COLOR_VECTOR[level[row][column]], screen=self.screen,
                           row=row, column=column) \
                        if level[row][column] >= 0 and level[row][column] <= COLUMNS \
                        else None

                # Add the bubble to the bubble list to check for collision
                if self.matrix[row][column] != None:
                    self.bubbleList.append(self.matrix[row][column])
                    idex = COLOR_VECTOR.index(self.matrix[row][column].color)
                    self.colorsUsed[idex] += 1

            row += 1

    def checkForCollision(self, bubble):

        hit = bubble.rect.collidelist(self.bubbleList)
        dreapta = False

        if hit != -1:
            bubbleHit = self.bubbleList[hit]
            row = bubbleHit.row
            column = bubbleHit.column

            print("dreapta : ", abs(bubble.rect.left - bubbleHit.rect.right))
            print("stanga : ", abs(bubble.rect.right - bubbleHit.rect.left))
            print("jos : ", abs(bubble.rect.top - bubbleHit.rect.bottom))

            print(bubbleHit.row, " ", bubbleHit.column)

            if abs(bubble.rect.top - bubbleHit.rect.bottom) in range(0, 20):
                print("jos")
                row += 1

            if abs(bubble.rect.left - bubbleHit.rect.right) in range(0, 20):
                print("dreapta")
                dreapta = True
                column += 1 if row % 2 == 0 else 0
            if abs(bubble.rect.right - bubbleHit.rect.left) in range(0, 20):
                print("stanga")
                dreapta = False
                column -= 1

            if row % 2 == 0 and not dreapta:
                column += 1

            if row % 2 != 0 and column == COLUMNS - 1:
                column -= 1

            # check for free space
            if self.matrix[row][column] == None:
                bubble.updateValues(row, column)
                self.matrix[row][column] = bubble
            elif dreapta and self.matrix[row][column + 1] == None:
                bubble.updateValues(row, column + 1)
                self.matrix[row][column + 1] = bubble
            elif not dreapta and self.matrix[row][column - 1] == None:
                bubble.updateValues(row, column - 1)
                self.matrix[row][column - 1] = bubble
            else:
                print("ERROR: Cant put the bubble in the matrix")
                return -1

            self.bubbleList.append(bubble)
            self.colorsUsed[COLOR_VECTOR.index(bubble.color)] += 1
            print("========================\n")
            return True

        return False

    def getDeletedBubbles(self):

        bubblesToDelete = []
        bubblesToDelete.append(self.bubbleList[-1])

        for bubble in bubblesToDelete:

            for row in range(-1, 2):
                for column in range(-1, 2):
                    if bubble.row % 2 != 0:
                        if row == 0 and column == 0:
                            continue
                        if row != 0 and column == -1:
                            continue
                        if bubble.column + column == COLUMNS - 1:
                            continue
                        if bubble.column + column == -1 or bubble.column + column == COLUMNS - 1:
                            continue

                        if self.matrix[bubble.row + row][bubble.column + column] != None:
                            neighbourBubble = self.matrix[bubble.row + row][bubble.column + column]
                            if neighbourBubble.color == bubble.color and neighbourBubble not in bubblesToDelete:
                                bubblesToDelete.append(neighbourBubble)
                    else:
                        if row == 0 and column == 0:
                            continue
                        if row != 0 and column == 1:
                            continue
                        if bubble.column + column == COLUMNS:
                            continue
                        if row != 0 and bubble.column == COLUMNS - 1:
                            continue
                        if bubble.column + column == -1 or bubble.column + column == COLUMNS:
                            continue

                        if self.matrix[bubble.row + row][bubble.column + column] != None:
                            neighbourBubble = self.matrix[bubble.row + row][bubble.column + column]
                            if neighbourBubble.color == bubble.color and neighbourBubble not in bubblesToDelete:
                                bubblesToDelete.append(neighbourBubble)

        if len(bubblesToDelete) > 2:
            return True, bubblesToDelete

        return False, bubblesToDelete

    def deleteBubbles(self, bubblesToDelete):
        score = len(bubblesToDelete) * 10

        for bubble in bubblesToDelete:
            if self.matrix[bubble.row][bubble.column] == None:
                print("ERROR, sapce allready empty. game.py/Table.deleteBubbles()")
                return
            else:
                self.matrix[bubble.row][bubble.column] = None
                self.bubbleList.remove(bubble)
                self.colorsUsed[COLOR_VECTOR.index(bubble.color)] -= 1
                print(self.colorsUsed)

        return score

    def printTable(self):
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                print(type(self.matrix[row][column]), end="")

            print("")
            row += 1


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

    def loadLevel(self, level):
        self.table.loadLevel("Levels/" + str(level) + ".txt")

    def loadShootingBubble(self):
        self.shootingBubble = self.nextShootingBubble  # self.nextShootingBubble
        self.shootingBubble.rect.centerx = self.shootingPoint.positionX
        self.shootingBubble.rect.centery = self.shootingPoint.positionY

    def loadNextShootingBubble(self):
        nArray = np.array(self.table.colorsUsed)
        indexes = np.where(nArray != 0)[0].tolist()
        colorUsed = random.choice(indexes)

        self.nextShootingBubble = Bubble(COLOR_VECTOR[colorUsed], self.screen, 0, 0)
        self.nextShootingBubble.rect.centerx = self.shootingPoint.positionX + 200
        self.nextShootingBubble.rect.centery = self.shootingPoint.positionY

    def draw(self):
        self.screen.fill(COLOR_BLACK)
        self.table.draw()
        self.shootingBubble.draw()
        self.nextShootingBubble.draw()
        self.score.draw()

    def run(self):
        self.loadLevel("level1")
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

            if shooting == True:
                self.shootingBubble.update()
                succes = self.table.checkForCollision(self.shootingBubble)

                if succes != False:
                    self.loadShootingBubble()
                    self.loadNextShootingBubble()
                    response, resultList = self.table.getDeletedBubbles()
                    if response == True:
                        scoreResult = self.table.deleteBubbles(resultList)
                        self.score.update(scoreResult)

                    shooting = False

                    print(self.table.colorsUsed)

            pygame.display.update()
            self.clock.tick(60)
