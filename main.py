from game import BubbleGame

if __name__ == "__main__":
    game = BubbleGame()
    game.run()


# gameMatrix = [ [0 for i in range(12 if j%2 == 0 else 11)] for j in range(10) ]
#
# row = 0
# for line in gameMatrix:
#     for column in range(len(line)):
#         print(gameMatrix[row][column], "  ", end="")
#     print("")
#     row += 1
