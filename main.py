import pygame
from game import Table, Score
from Utyls.variables import *

# Initialize the pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Width, height

gameTable = Table(screen)
score = Score(screen)

gameTable.loadLevel("Levels/level1.txt")

running = True
while running:
    gameTable.draw()
    score.draw()
    score.totalScore+=1
    score.update()

    x, y = pygame.mouse.get_pos()
    # print(x," ", y)


    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False






# 10 x 12 matrix

# gameMatrix = [ [0 for i in range(12 if j%2 == 0 else 11)] for j in range(10) ]
#
# row = 0
# for line in gameMatrix:
#     for column in range(len(line)):
#         print(gameMatrix[row][column], "  ", end="")
#     print("")
#     row += 1