import pygame.font
from Utyls.variables import *
from Bubble import Bubble


# Table component
class Table(object):
    def __init__(self, screen):
        self.screen = screen
        self.matrix = self.initMatrix()

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
            row += 1

    def printTable(self):
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                print(type(self.matrix[row][column]), end="")

            print("")
            row += 1


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

