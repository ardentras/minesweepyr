###########################################################
# Filename: main.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/30/2020
#
# entrypoint and main loop
#

import sys, pygame
import colors, board

def processClick(event, gameBoard):
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    x,y = event.pos
    bcw, bch = gameBoard.getTileBoardRelativeCenter()
    x = int(x - bcw)
    y = int(y - bch)

    boardRect = gameBoard.getTileBoard().get_rect()
    leftButtonRect = gameBoard.getLeftButton().get_rect()
    rightButtonRect = gameBoard.getRightButton().get_rect()
    if boardRect.collidepoint((x, y)):
        scaledX = int(x / gameBoard.getTileSize())
        scaledY = int(y / gameBoard.getTileSize())

        if not gameBoard.isPlayable():
            gameBoard.fillBoard((scaledX, scaledY))

        if pressed1:
            if not gameBoard.getTile(scaledX, scaledY).isFlagged():
                gameBoard.uncover(scaledX, scaledY)
        elif pressed3:
            if not gameBoard.getTile(scaledX, scaledY).isUncovered():
                gameBoard.flipFlagged(scaledX, scaledY)
    elif leftButtonRect.move(gameBoard.getDifficultyLeftButtonPosition()).collidepoint(event.pos):
        gameBoard.difficultyRotateLeft()
    elif rightButtonRect.move(gameBoard.getDifficultyRightButtonPosition()).collidepoint(event.pos):
        gameBoard.difficultyRotateRight()
    elif leftButtonRect.move(gameBoard.getBoardSizeLeftButtonPosition()).collidepoint(event.pos):
        gameBoard.boardSizeRotateLeft()
    elif rightButtonRect.move(gameBoard.getBoardSizeRightButtonPosition()).collidepoint(event.pos):
        gameBoard.boardSizeRotateRight()

pygame.init()

pygame.display.set_caption("Minesweepyr")
screen = pygame.display.set_mode((640, 480))

gameBoard = board.Board(16, screen.get_size())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            processClick(event, gameBoard)
                
    screen.fill(colors.GRAY)
    gameBoard.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()