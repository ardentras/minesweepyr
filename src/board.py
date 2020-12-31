###########################################################
# Filename: board.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/30/2020
#
# Everything drawn to the screen that's related to the
# game board and game actions
#

import pygame
import colors, tiles
import random
from collections import deque

class Difficulty():
    def __init__(self, name, modifier):
        self.name = name
        self.modifier = modifier
    
    def getName(self):
        return self.name
    
    def getModifier(self):
        return self.modifier

MIN_MINE_PROBABILITY = 0.05
INVALID_PROBABILITY = 2

TEXT_COLOR = colors.WHITE
TEXT_MARGIN = 5

FONT = "Courier New"

class Board():
    def __init__(self, tileSize, screenSize):
        self.playable = False
        self.won = False

        self.DIFFICULTIES = deque()
        self.DIFFICULTIES.append(Difficulty("EASY", 0.05))
        self.DIFFICULTIES.append(Difficulty("MEDIUM", 0.1))
        self.DIFFICULTIES.append(Difficulty("HARD", 0.2))
        self.DIFFICULTIES.append(Difficulty("PRO", 0.35))

        self.BOARD_SIZES = deque()
        self.BOARD_SIZES.append((128, 128 * 3 / 2))
        self.BOARD_SIZES.append((128 * 3 / 2, 128 * 2))
        self.BOARD_SIZES.append((128 * 2, 128 * 3))
        self.BOARD_SIZES.append((128 * 3, 128 * 3))

        self.tileGroup = pygame.sprite.Group()
        self.mineGroup = pygame.sprite.Group()

        self.flaggable = 0
        self.setTileSize(tileSize)
        self.screenSize = screenSize
        self.tileBoardSize = self.BOARD_SIZES.popleft()
        self.difficulty = self.DIFFICULTIES.popleft()
       
        self.winText = self.monospaceFont.render("Congratulations, you won!", True, TEXT_COLOR)
        self.howToPlayText = self.monospaceFont.render("Left click to reveal. Right click to flag.", True, TEXT_COLOR)
        self.playAgainText = self.monospaceFont.render("Click anywhere on the board to start.", True, TEXT_COLOR)
        self.difficultyText = self.monospaceFont.render("DIFFICULTY", True, TEXT_COLOR)
        self.boardSizeText = self.monospaceFont.render("BOARD SIZE", True, TEXT_COLOR)

        self.leftButton = self.monospaceFont.render("<", True, TEXT_COLOR)
        self.rightButton = self.monospaceFont.render(">", True, TEXT_COLOR)
        
        self.difficultyTextPosition = ((self.screenSize[0] / 2) - (self.difficultyText.get_width() / 2), self.screenSize[1] - ((self.difficultyText.get_height() + TEXT_MARGIN) * 2))
        self.difficultyLeftButtonPosition = (self.difficultyTextPosition[0] - self.leftButton.get_width() - TEXT_MARGIN, self.difficultyTextPosition[1])
        self.difficultyRightButtonPosition = (self.difficultyTextPosition[0] + self.difficultyText.get_width() + TEXT_MARGIN, self.difficultyTextPosition[1])

        self.boardSizeRightButtonPosition = (self.difficultyLeftButtonPosition[0] - self.rightButton.get_width() - (TEXT_MARGIN * 3), self.difficultyTextPosition[1])
        self.boardSizeTextPosition = (self.boardSizeRightButtonPosition[0] - self.boardSizeText.get_width() - TEXT_MARGIN, self.boardSizeRightButtonPosition[1])
        self.boardSizeLeftButtonPosition = (self.boardSizeTextPosition[0] - self.leftButton.get_width() - TEXT_MARGIN, self.boardSizeTextPosition[1])

        self.updateTileBoard()
        
    def draw(self, screen):
        self.tileGroup.draw(self.tileBoard)
        self.mineGroup.draw(self.tileBoard)
        screen.blit(self.tileBoard, self.getTileBoardRelativeCenter())

        difficulty = self.monospaceFont.render(self.difficulty.getName(), True, TEXT_COLOR)
        screen.blit(difficulty, ((self.screenSize[0] / 2) - (difficulty.get_width() / 2), self.screenSize[1] - (difficulty.get_height() + TEXT_MARGIN)))
        screen.blit(self.leftButton, self.difficultyLeftButtonPosition)
        screen.blit(self.difficultyText, self.difficultyTextPosition)
        screen.blit(self.rightButton, self.difficultyRightButtonPosition)

        tileBoardSize = self.monospaceFont.render("%d x %d" % self.tileBoardSize, True, TEXT_COLOR)
        screen.blit(self.leftButton, self.boardSizeLeftButtonPosition)
        screen.blit(self.boardSizeText, self.boardSizeTextPosition)
        screen.blit(self.rightButton, self.boardSizeRightButtonPosition)
        screen.blit(tileBoardSize, ((self.boardSizeTextPosition[0] + (self.boardSizeText.get_width() / 2)) - (tileBoardSize.get_width() / 2), self.boardSizeTextPosition[1] + TEXT_MARGIN + tileBoardSize.get_height()))

        if self.won:
            screen.blit(self.winText, ((self.screenSize[0] / 2) - (self.winText.get_width() / 2), TEXT_MARGIN))
        else:
            flagsLeftText = self.monospaceFont.render("Flags left: %s" % (self.flaggable), True, TEXT_COLOR)
            screen.blit(flagsLeftText, ((self.screenSize[0] / 2) - (flagsLeftText.get_width() / 2), TEXT_MARGIN))

        if self.playable:
            screen.blit(self.howToPlayText, ((self.screenSize[0] / 2) - (self.howToPlayText.get_width() / 2), (self.howToPlayText.get_height() + (TEXT_MARGIN * 2))))
        else:
            screen.blit(self.tileBoardOverlay, self.getTileBoardRelativeCenter())
            screen.blit(self.playAgainText, ((self.screenSize[0] / 2) - (self.playAgainText.get_width() / 2), (self.playAgainText.get_height() + (TEXT_MARGIN * 2))))

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
                    tile = tiles.MineTile(pos=(x, y), font=self.monospaceFont, color=colors.WHITE)
                    self.mineGroup.add(tile)
                else:
                    tile = tiles.NumberTile(value=board[x][y], pos=(x, y), font=self.monospaceFont, color=colors.WHITE)
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
    
    def isPlayable(self):
        return self.playable

    def getLeftButton(self):
        return self.leftButton

    def getRightButton(self):
        return self.rightButton

    def getDifficultyTextPosition(self):
        return self.difficultyTextPosition

    def getDifficultyLeftButtonPosition(self):
        return self.difficultyLeftButtonPosition

    def getDifficultyRightButtonPosition(self):
        return self.difficultyRightButtonPosition

    def difficultyRotateLeft(self):
        self.DIFFICULTIES.appendleft(self.difficulty)
        self.difficulty = self.DIFFICULTIES.pop()
        self.resetGame()

    def difficultyRotateRight(self):
        self.DIFFICULTIES.append(self.difficulty)
        self.difficulty = self.DIFFICULTIES.popleft()
        self.resetGame()

    def getBoardSize(self):
        return self.tileBoardSize

    def getBoardSizeTextPosition(self):
        return self.boardSizeTextPosition

    def getBoardSizeLeftButtonPosition(self):
        return self.boardSizeLeftButtonPosition

    def getBoardSizeRightButtonPosition(self):
        return self.boardSizeRightButtonPosition

    def boardSizeRotateLeft(self):
        self.BOARD_SIZES.appendleft(self.tileBoardSize)
        self.tileBoardSize = self.BOARD_SIZES.pop()
        self.updateTileBoard()

    def boardSizeRotateRight(self):
        self.BOARD_SIZES.append(self.tileBoardSize)
        self.tileBoardSize = self.BOARD_SIZES.popleft()
        self.updateTileBoard()
    
    def updateTileBoard(self):
        self.resetGame()
        self.tileBoard = pygame.Surface(self.tileBoardSize)
        self.tileBoardOverlay = pygame.Surface(self.tileBoardSize)
        self.tileBoardOverlay.set_alpha(64, pygame.RLEACCEL)
        self.tileBoardOverlay.fill(colors.BLACK)