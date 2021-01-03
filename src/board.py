###########################################################
# Filename: board.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/31/2020
#
# Everything drawn to the screen that's related to the
# game board and game actions
#

import pygame
import colors, tiles
import random

MIN_MINE_PROBABILITY = 0.05
INVALID_PROBABILITY = 2

FONT = "Courier New"

class Board():
    def __init__(self, tileSize, screenSize, tileBoardSize, difficulty, theme):
        self.playable = False
        self.won = False

        self.tileGroup = pygame.sprite.Group()
        self.mineGroup = pygame.sprite.Group()

        self.tileMatrix = []

        self.flaggable = 0
        self.setTileSize(tileSize)
        self.tileBoardSize = tileBoardSize
        self.screenSize = screenSize

        self.difficulty = difficulty
        
        self.theme = theme

        self.updateTileBoard()
        
    def draw(self, screen):
        self.tileBoard.fill(self.theme.boardColor)
        self.tileGroup.draw(self.tileBoard)
        self.mineGroup.draw(self.tileBoard)
        screen.blit(self.tileBoard, self.getTileBoardRelativeCenter())

        if not self.playable:
            self.tileBoardOverlay.fill(self.theme.boardColor)
            screen.blit(self.tileBoardOverlay, self.getTileBoardRelativeCenter())

    def processClick(self, event):
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
        x,y = event.pos
        bcw, bch = self.getTileBoardRelativeCenter()
        x = int(x - bcw)
        y = int(y - bch)

        boardRect = self.getTileBoard().get_rect()
        if boardRect.collidepoint((x, y)):
            scaledX = int(x / self.getTileSize())
            scaledY = int(y / self.getTileSize())

            if not self.playable:
                self.fillBoard((scaledX, scaledY))

            if pressed1:
                if not self.getTile(scaledX, scaledY).isFlagged():
                    self.uncover(scaledX, scaledY)
            elif pressed3:
                if not self.getTile(scaledX, scaledY).isUncovered():
                    self.flipFlagged(scaledX, scaledY)

    def fillBoard(self, startPos):
        self.resetGame()

        mineProb = MIN_MINE_PROBABILITY
        random.seed()

        w, h = self.getScaledBounds()
        self.totalTiles = w * h
        self.flaggable = int(w * h * self.difficulty.getModifier())

        self.tileMatrix = [[object for e in range(h)] for e in range(w)]
        mineMatrix = [[random.random() for e in range(h)] for e in range(w)]
        board = [[0 for e in range(h)] for e in range(w)]

        # Ensures that first click always starts in a blank space
        for x in range(startPos[0] - 1 if startPos[0] - 1 > 0 else 0, startPos[0] + 2 if startPos[0] + 2 < w else w):
            for y in range(startPos[1] - 1 if startPos[1] - 1 > 0 else 0, startPos[1] + 2 if startPos[1] + 2 < h else h):
                mineMatrix[x][y] = INVALID_PROBABILITY

        # Iterate over the probability map and set mines accordingly.
        # Start with a minimum probability threshold and while the total number
        # has not been reached, increment the threshold until all mines are set.
        while self.mineCount < self.flaggable:
            for x in range(w):
                for y in range(h):
                    if mineMatrix[x][y] < mineProb and self.mineCount < self.flaggable:
                        self.mineCount = self.mineCount + 1
                        mineMatrix[x][y] = INVALID_PROBABILITY
                        board[x][y] = tiles.MINE

                        for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
                            for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                                if board[x1][y1] < 8:
                                    board[x1][y1] = board[x1][y1] + 1

                    if self.mineCount >= self.flaggable:
                        break
                if self.mineCount >= self.flaggable:
                    break
            if self.mineCount >= self.flaggable:
                break
            
            mineProb = mineProb + 0.05
            
        for x in range(w):
            for y in range(h):
                tile = object

                if board[x][y] == tiles.MINE:
                    tile = tiles.MineTile(pos=(x, y), theme=self.theme)
                    self.mineGroup.add(tile)
                else:
                    tile = tiles.NumberTile(value=board[x][y], pos=(x, y), theme=self.theme)
                    self.tileGroup.add(tile)

                self.tileMatrix[x][y] = tile

        self.playable = True

    def updateSurrounding(self, x, y, w, h):
        for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
            for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                if self.tileMatrix[x1][y1].isUncovered() == False:
                    self.uncoverTile(x1, y1)

                    if self.tileMatrix[x1][y1].getValue() == 0:
                        self.updateSurrounding(x1, y1, w, h)
    
    def revealMines(self):
        self.playable = False
        w, h = self.getScaledBounds()
        for x in range(w):
            for y in range(h):
                if self.tileMatrix[x][y].getValue() == 9:
                    self.tileMatrix[x][y].setFlagged(False)
                    self.tileMatrix[x][y].setUncovered(True)

    def uncoverTile(self, x, y):
        if not self.tileMatrix[x][y].isUncovered():
            self.countUncoveredTiles = self.countUncoveredTiles + 1
            self.tileMatrix[x][y].setUncovered(True)

    def uncover(self, x, y):
        self.uncoverTile(x,y)
        
        if self.tileMatrix[x][y].getValue() == 0:
            w, h = self.getScaledBounds()
            self.updateSurrounding(x, y, w, h)

        if self.tileMatrix[x][y].getValue() == 9:
            self.revealMines()
        elif self.countUncoveredTiles + self.mineCount == self.totalTiles:
            self.win()

    def flipFlagged(self, x, y):
        inc = 1 if self.tileMatrix[x][y].isFlagged() else -1
        self.flaggable = self.flaggable + inc
        self.tileMatrix[x][y].setFlagged(not self.tileMatrix[x][y].isFlagged())

        if self.flaggable == 0:
            allFlagged = True
            for mine in self.mineGroup:
                if not mine.isFlagged():
                    allFlagged = False
                    break
            
            if allFlagged:
                self.win()
    
    def updateTileBoard(self):
        self.resetGame()
        self.tileBoard = pygame.Surface(self.tileBoardSize)
        self.tileBoardOverlay = pygame.Surface(self.tileBoardSize)
        self.tileBoardOverlay.set_alpha(64, pygame.RLEACCEL)

    def win(self):
        self.playable = False
        self.won = True

    def resetGame(self):
        self.won = False
        self.playable = False
        self.tileGroup.empty()
        self.mineGroup.empty()
        self.mineCount = 0
        self.countUncoveredTiles = 0

    def getTile(self, x, y):
        return self.tileMatrix[x][y]

    def getTileBoard(self):
        return self.tileBoard

    def getTileBoardRelativeCenter(self):
        return ((self.screenSize[0] / 2) - (self.tileBoard.get_width() / 2), (self.screenSize[1] / 2) - (self.tileBoard.get_height() / 2))

    def getTileSize(self):
        return self.tileSize

    def setTileSize(self, tileSize):
        self.tileSize = tileSize
        self.monospaceFont = pygame.font.SysFont(FONT, int(self.tileSize * .9))

    def getScaledBounds(self):
        w = int(self.tileBoard.get_width() / self.tileSize)
        if self.tileBoard.get_width() % self.tileSize != 0: w = w - 1
        h = int(self.tileBoard.get_height() / self.tileSize)
        if self.tileBoard.get_height() % self.tileSize != 0: h = h - 1

        return (w,h)

    def getFlagsLeft(self):
        return self.flaggable

    def hasWon(self):
        return self.won
    
    def isPlayable(self):
        return self.playable

    def getTileBoardSize(self):
        return self.tileBoardSize

    def setTileBoardSize(self, tbs):
        self.tileBoardSize = tbs
        self.updateTileBoard()

    def getDifficulty(self):
        return self.difficulty
    
    def setDifficulty(self, d):
        self.difficulty = d
        self.resetGame()

    def setTheme(self, theme):
        self.theme = theme
        for tileRow in self.tileMatrix:
            for tile in tileRow:
                tile.setTheme(self.theme)
                tile.redraw()
