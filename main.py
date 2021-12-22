import pygame
from game import Table
from components import Score, ShootingPoint, Bubble
from Utyls.variables import *

# Initialize the pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Width, height

gameTable = Table(screen)
score = Score(screen)
cannon = ShootingPoint()

gameTable.loadLevel("Levels/level1.txt")
b = Bubble(COLOR_PURPLE, screen, 0, 0)

b.rect.centerx = cannon.positionX
b.rect.centery = cannon.positionY

running = True
s = False
clock = pygame.time.Clock()
while running:
    screen.fill(COLOR_BLACK)
    b.draw()
    gameTable.draw()
    score.draw()
    # score.totalScore+=1
    # score.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP and not s:
            cannon.update()
            b.shootingAngle = cannon.angle
            s = True

    if s:
        b.update()
        succes = gameTable.checkForCollision(b)

        if succes == True:
            s = False
            b =  Bubble(COLOR_PURPLE, screen, 0, 0)
            b.rect.centerx = cannon.positionX
            b.rect.centery = cannon.positionY
            b.draw()
        elif succes == -1:
            s = False
            b = Bubble(COLOR_PURPLE, screen, 0, 0)
            b.rect.centerx = cannon.positionX
            b.rect.centery = cannon.positionY
            b.draw()




    pygame.display.update()
    clock.tick(60)
# 10 x 12 matrix

# gameMatrix = [ [0 for i in range(12 if j%2 == 0 else 11)] for j in range(10) ]
#
# row = 0
# for line in gameMatrix:
#     for column in range(len(line)):
#         print(gameMatrix[row][column], "  ", end="")
#     print("")
#     row += 1
