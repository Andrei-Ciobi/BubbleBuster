from Utyls.variables import *
from components import Bubble

# Table component
class Table(object):
    def __init__(self, screen):
        self.screen = screen
        self.matrix = self.initMatrix()
        self.bubbleList = []
        self.colorsUsed = [0 for i in range(COLUMNS)]
        self.lose = False

    # Resets the table to and empty table
    def initializeTableValues(self):
        self.matrix = self.initMatrix()
        self.bubbleList = []
        self.colorsUsed = [0 for i in range(COLUMNS)]
        self.lose = False

    # Initiate the matrix to a null matrix
    def initMatrix(self):
        return [[None for i in range(COLUMNS if j % 2 == 0 else COLUMNS - 1)] for j in range(ROWS)]

    # Draw the table components
    def draw(self):
        # Draw the matrix

        for row, line in enumerate(self.matrix):
            for column in range(len(line)):
                if self.matrix[row][column] != None:
                    self.matrix[row][column].draw()

    # Loads a predef level into the self.matrix atribute
    def loadLevel(self, fileName):

        self.initializeTableValues()

        # Load the level
        file = open(fileName, 'r')
        level = [[int(num) for num in line.split()] for line in file]

        # Update to the curent level
        for row, line in enumerate(level):
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

    # Checks if the shooted bubble hits another bubble
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

            if row >= ROWS:
                self.lose = True
                return False

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
                        if row == 0 and (bubble.column + column == COLUMNS - 1 or bubble.column + column == -1):
                            continue
                        if row != 0 and (bubble.column + column == -1 or bubble.column + column == COLUMNS):
                            continue
                        if row + bubble.row >= ROWS:
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
                        if row == 0 and (bubble.column + column == COLUMNS or bubble.column + column == -1):
                            continue
                        if row != 0 and (bubble.column + column == -1 or bubble.column + column == COLUMNS - 1):
                            continue
                        if row + bubble.row >= ROWS:
                            continue

                        if self.matrix[bubble.row + row][bubble.column + column] != None:
                            neighbourBubble = self.matrix[bubble.row + row][bubble.column + column]
                            if neighbourBubble.color == bubble.color and neighbourBubble not in bubblesToDelete:
                                bubblesToDelete.append(neighbourBubble)

        if len(bubblesToDelete) > 2:
            return True, bubblesToDelete

        return False, bubblesToDelete

    # Goes throw the matrix and gets the connected bubbles
    def getConnectedBubbles(self):

        connectedBubbles = []

        for bubble in self.matrix[0]:
            if bubble is not None:
                connectedBubbles.append(bubble)

        for bubble in connectedBubbles:
            for row in range(-1, 2):
                for column in range(-1, 2):
                    if bubble.row % 2 != 0:
                        if row == 0 and column == 0:
                            continue
                        if row != 0 and column == -1:
                            continue
                        if row == 0 and (bubble.column + column == COLUMNS - 1 or bubble.column + column == -1):
                            continue
                        if row != 0 and (bubble.column + column == -1 or bubble.column + column == COLUMNS):
                            continue

                        if self.matrix[bubble.row + row][bubble.column + column] != None:
                            neighbourBubble = self.matrix[bubble.row + row][bubble.column + column]
                            if neighbourBubble not in connectedBubbles:
                                connectedBubbles.append(neighbourBubble)
                    else:
                        if row == 0 and column == 0:
                            continue
                        if row != 0 and column == 1:
                            continue
                        if row == 0 and (bubble.column + column == COLUMNS or bubble.column + column == -1):
                            continue
                        if row != 0 and (bubble.column + column == -1 or bubble.column + column == COLUMNS - 1):
                            continue

                        if self.matrix[bubble.row + row][bubble.column + column] != None:
                            neighbourBubble = self.matrix[bubble.row + row][bubble.column + column]
                            if neighbourBubble not in connectedBubbles:
                                connectedBubbles.append(neighbourBubble)
        return connectedBubbles

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

    # Deletes the bubbles from the matrix that are not in the connected list of bubbles
    def deleteFloatingBubbles(self, connectedBubbles):
        score = 0

        for row, line in enumerate(self.matrix):
            for column in range(len(line)):
                bubble = self.matrix[row][column]

                if bubble is not None:
                    if bubble not in connectedBubbles:
                        self.matrix[row][column] = None
                        self.bubbleList.remove(bubble)
                        self.colorsUsed[COLOR_VECTOR.index(bubble.color)] -= 1
                        score += 10
        return score
