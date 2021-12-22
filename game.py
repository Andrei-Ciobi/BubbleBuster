import pygame.font
from Utyls.variables import *
from components import Bubble


# Table component
class Table(object):
    def __init__(self, screen):
        self.screen = screen
        self.matrix = self.initMatrix()
        self.bubbleList = []

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
            print("========================\n")
            return True

        return False

    def printTable(self):
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                print(type(self.matrix[row][column]), end="")

            print("")
            row += 1
