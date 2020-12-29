###########################################################
# Filename: board.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#

import pygame
import tiles
import random

DIFFICULTY_EASY = 0.05
DIFFICULTY_MED = 0.1
DIFFICULTY_HARD = 0.2
DIFFICULTY_PRO = 0.35

MIN_MINE_PROBABILITY = 0.05
INV_PROB = 2
MINE = 9

class Board():
    def __init__(self, tileSize, boardSize, screenSize):
        self.setTileSize(tileSize)
        self.screenSize = screenSize
        self.tileBoardSize = boardSize
        self.tileBoard = pygame.Surface(self.tileBoardSize)
        
    def draw(self, screen):
        self.tileGroup.draw(self.tileBoard)
        self.mineGroup.draw(self.tileBoard)
        screen.blit(self.tileBoard, self.getTileBoardRelativeCenter())

    def fillBoard(self, difficulty = DIFFICULTY_EASY):
        self.tileGroup = pygame.sprite.Group()
        self.mineGroup = pygame.sprite.Group()
        self.mineCount = 0

        mineProb = MIN_MINE_PROBABILITY
        random.seed()

        w, h = self.getScaledBounds()
        self.totalTiles = w * h
        self.flagable = int(w * h * difficulty)
        print("total mines:", self.flagable)
        print("total tiles:", self.totalTiles)

        self.tileMatrix = [[object for e in range(h)] for e in range(w)]
        mineMatrix = [[random.random() for e in range(h)] for e in range(w)]
        board = [[0 for e in range(h)] for e in range(w)]

        # Iterate over the probability map and set mines accordingly.
        # Start with a minimum probability threshold and while the total number
        # has not been reached, increment the threshold until all mines are set.
        while self.mineCount < self.flagable:
            for x in range(w):
                for y in range(h):
                    if mineMatrix[x][y] < mineProb and self.mineCount < self.flagable:
                        self.mineCount = self.mineCount + 1
                        mineMatrix[x][y] = INV_PROB
                        board[x][y] = MINE

                        for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
                            for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                                if board[x1][y1] < 8:
                                    board[x1][y1] = board[x1][y1] + 1

                    if self.mineCount >= self.flagable:
                        break
                if self.mineCount >= self.flagable:
                    break
            if self.mineCount >= self.flagable:
                break
            
            mineProb = mineProb + 0.05
            
        for x in range(w):
            for y in range(h):
                tile = object

                if board[x][y] == MINE:
                    tile = tiles.Tile(value="X", pos=(x, y), font=self.monospaceFont)
                    self.mineGroup.add(tile)
                else:
                    tile = tiles.Tile(value=str(board[x][y]), pos=(x, y), font=self.monospaceFont)
                    self.tileGroup.add(tile)

                self.tileMatrix[x][y] = tile

    def updateSurrounding(self, x, y, w, h):
        for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
            for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                tile = self.tileMatrix[x1][y1]
                
                if tile.getUncovered() == False:
                    self.tileMatrix[x1][y1].setUncovered(True)
                    
                    if tile.getValue() == 0:
                        self.updateSurrounding(x1, y1, w, h)
    
    def revealMines(self):
        w, h = self.getScaledBounds()
        for x in range(w):
            for y in range(h):
                if self.tileMatrix[x][y].getValue() == 9:
                    self.tileMatrix[x][y].setUncovered(True)

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
        self.monospaceFont = pygame.font.SysFont("Consolas", int(self.tileSize * .9), True)

    def getScaledBounds(self):
        w = int(self.tileBoard.get_width() / self.tileSize)
        if self.tileBoard.get_width() % self.tileSize != 0: w = w - 1
        h = int(self.tileBoard.get_height() / self.tileSize)
        if self.tileBoard.get_height() % self.tileSize != 0: h = h - 1

        return (w,h)