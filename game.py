from Utyls.variables import *
from Bubble import Bubble


class Table:
    def __init__(self, screen):
        self.screen = screen
        self.matrix = self.initMatrix()

    # Initiate the matrix, must be changes with predef levels !!!!
    def initMatrix(self):
        return [[Bubble(screen=self.screen, color=RED, row=j, column=i) for i in
                 range(COLUMNS if j % 2 == 0 else COLUMNS - 1)] for j in range(ROWS)]

    # Draw the table components
    def draw(self):
        # Draw the matrix
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                self.matrix[row][column].draw()
            row += 1

    def printTable(self):
        row = 0
        for line in self.matrix:
            for column in range(len(line)):
                print(self.matrix[row][column])
            row += 1
