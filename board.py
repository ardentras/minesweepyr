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
INVALID_PROBABILITY = 2

TEXT_COLOR = (255, 255, 255)
TEXT_TOP_MARGIN = 5

class Board():
    def __init__(self, tileSize, boardSize, screenSize):
        self.playable = False
        self.won = False

        self.flaggable = 0
        self.setTileSize(tileSize)
        self.screenSize = screenSize
        self.tileBoardSize = boardSize
        self.tileBoard = pygame.Surface(self.tileBoardSize)

        self.tileGroup = pygame.sprite.Group()
        self.mineGroup = pygame.sprite.Group()
       
        self.winText = self.monospaceFont.render("Congratulations, you won!", True, TEXT_COLOR)
        self.playAgainText = self.monospaceFont.render("Click anywhere on the board to start.", True, TEXT_COLOR)

        self.difficulty = DIFFICULTY_EASY
        
    def draw(self, screen):
        self.tileGroup.draw(self.tileBoard)
        self.mineGroup.draw(self.tileBoard)
        screen.blit(self.tileBoard, self.getTileBoardRelativeCenter())

        if not self.playable:
            screen.blit(self.playAgainText, ((self.screenSize[0] / 2) - (self.playAgainText.get_width() / 2), (self.playAgainText.get_height() + (TEXT_TOP_MARGIN * 2))))

        if self.won:
            screen.blit(self.winText, ((self.screenSize[0] / 2) - (self.winText.get_width() / 2), TEXT_TOP_MARGIN))
        else:
            flagsLeftText = self.monospaceFont.render("Flags left: %s" % (self.flaggable), True, TEXT_COLOR)
            screen.blit(flagsLeftText, ((self.screenSize[0] / 2) - (flagsLeftText.get_width() / 2), TEXT_TOP_MARGIN))

    def fillBoard(self, startPos):
        self.won = False
        self.tileGroup.empty()
        self.mineGroup.empty()
        self.mineCount = 0
        self.countUncoveredTiles = 0

        mineProb = MIN_MINE_PROBABILITY
        random.seed()

        w, h = self.getScaledBounds()
        self.totalTiles = w * h
        self.flaggable = int(w * h * self.difficulty)
        print("total mines:", self.flaggable)
        print("total tiles:", self.totalTiles)

        self.tileMatrix = [[object for e in range(h)] for e in range(w)]
        mineMatrix = [[random.random() for e in range(h)] for e in range(w)]
        board = [[0 for e in range(h)] for e in range(w)]

        mineMatrix[startPos[0]][startPos[1]] = INVALID_PROBABILITY

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
                    tile = tiles.MineTile(pos=(x, y), font=self.monospaceFont)
                    self.mineGroup.add(tile)
                else:
                    tile = tiles.NumberTile(value=board[x][y], pos=(x, y), font=self.monospaceFont)
                    self.tileGroup.add(tile)

                self.tileMatrix[x][y] = tile

        self.playable = True

    def updateSurrounding(self, x, y, w, h):
        for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
            for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                if self.tileMatrix[x1][y1].isUncovered() == False:
                    self.setUncovered(x1, y1)
    
    def revealMines(self):
        self.playable = False
        w, h = self.getScaledBounds()
        for x in range(w):
            for y in range(h):
                if self.tileMatrix[x][y].getValue() == 9:
                    self.tileMatrix[x][y].setUncovered(True)

    def setUncovered(self, x, y):
        self.countUncoveredTiles = self.countUncoveredTiles + 1
        self.tileMatrix[x][y].setUncovered(True)
        
        if self.tileMatrix[x][y].getValue() == 9:
            self.revealMines()
        elif self.tileMatrix[x][y].getValue() == 0:
            w, h = self.getScaledBounds()
            self.updateSurrounding(x, y, w, h)

        if self.countUncoveredTiles + self.mineCount == self.totalTiles:
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

    def win(self):
        self.playable = False
        self.won = True

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
        self.monospaceFont = pygame.font.SysFont("Consolas", int(self.tileSize * .9))

    def getScaledBounds(self):
        w = int(self.tileBoard.get_width() / self.tileSize)
        if self.tileBoard.get_width() % self.tileSize != 0: w = w - 1
        h = int(self.tileBoard.get_height() / self.tileSize)
        if self.tileBoard.get_height() % self.tileSize != 0: h = h - 1

        return (w,h)
    
    def isPlayable(self):
        return self.playable

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty