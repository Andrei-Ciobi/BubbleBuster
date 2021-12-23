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

    # Checks if the shooted bubble hits te top of the window
    def checkForTopCollision(self, bubble):

        if bubble.rect.top < REC_HEIGHT / 2:
            row = 0
            column = round((bubble.rect.centerx - (REC_WIDTH / 2)) / SPACE_WIDTH)

            # check for free space
            if self.matrix[row][column] == None:
                bubble.updateValues(row, column)
                self.matrix[row][column] = bubble
            elif self.matrix[row][column + 1] == None:
                bubble.updateValues(row, column + 1)
                self.matrix[row][column + 1] = bubble
            elif self.matrix[row][column - 1] == None:
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

    # Checks if the shooted bubble hits something
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

    # Returns a list of the connected bubbles starting from the last bubble shooted
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

    # Deletes the given list of bubbles
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

        return score


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

    # Draws the components on the screen
    def draw(self):
        self.screen.fill(COLOR_BLACK)
        self.table.draw()
        self.shootingBubble.draw()
        self.nextShootingBubble.draw()
        self.score.draw()

    def run(self):
        self.loadLevel("level2")
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

                    # Generate new shooting bubble
                    self.loadShootingBubble()
                    self.loadNextShootingBubble()

                    # We no longer shoot
                    shooting = False
                    # print(self.table.colorsUsed)

            # update the window every 60 FPS
            pygame.display.update()
            self.clock.tick(120)
