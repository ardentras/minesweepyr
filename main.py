###########################################################
# Filename: main.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#

import sys, pygame
import board, tiles

pygame.init()

running = True

size = width, height = 640, 480

screen = pygame.display.set_mode(size)

gameBoard = board.Board(16, (128 * 2, 128 * 3))
bcw, bch = gameBoard.getTileBoardRelativeCenter(width, height)
gameBoard.fillBoard()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
            x,y = event.pos
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
                
    screen.fill((127,127,127))
    gameBoard.draw()
    screen.blit(gameBoard.getTileBoard(), (bcw, bch))
    
    pygame.display.flip()

pygame.quit()
sys.exit()