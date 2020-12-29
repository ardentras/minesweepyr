###########################################################
# Filename: main.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#

import sys, pygame
import board

def processClick(event, gameBoard):
    pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
    x,y = event.pos
    bcw, bch = gameBoard.getTileBoardRelativeCenter()
    x = int(x - bcw)
    y = int(y - bch)
    boardRect = gameBoard.getTileBoard().get_rect()
    if boardRect.collidepoint((x, y)):
        scaledX = int(x / gameBoard.getTileSize())
        scaledY = int(y / gameBoard.getTileSize())
        tile = gameBoard.getTile(scaledX, scaledY)
        
        if pressed1:
            if tile.getValue() == 0:
                w, h = gameBoard.getScaledBounds()
                tileMatrix = gameBoard.updateSurrounding(scaledX, scaledY, w, h)
            else:
                tile.setUncovered(True)
                if tile.getValue() == 9:
                    gameBoard.revealMines()
        elif pressed3:
            tile.setFlagged(not tile.getFlagged())

pygame.init()

screen = pygame.display.set_mode((640, 480))

gameBoard = board.Board(16, (128 * 3, 128 * 3), screen.get_size())
gameBoard.fillBoard()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            processClick(event, gameBoard)
                
    screen.fill((127,127,127))
    gameBoard.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()