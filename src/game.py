###########################################################
# Filename: game.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/31/2020
#
# Visual elements outside of the tile board
#

import pygame
import board, colors
import json
from collections import deque

FONT = "Courier New"

SETTINGS_FILENAME = 'settings.json'
TEXT_COLOR = colors.WHITE
TEXT_MARGIN = 5

class Difficulty():
    def __init__(self, name, modifier):
        self.name = name
        self.modifier = modifier
    
    def getName(self):
        return self.name
    
    def getModifier(self):
        return self.modifier

class Game():
    def __init__(self, tileSize, screenSize):
        settingsText = ""
        with open(SETTINGS_FILENAME, "r") as inFile:
            settingsText = inFile.read()
        settings = json.loads(settingsText)

        self.DIFFICULTIES = deque()
        for difficulty in settings['difficulties']:
            self.DIFFICULTIES.append(Difficulty(difficulty['name'], difficulty['modifier']))

        self.BOARD_SIZES = deque()
        for boardSize in settings['boardSizes']:
            self.BOARD_SIZES.append((boardSize[0], boardSize[1]))

        self.screenSize = screenSize
        self.gameBoard = board.Board(tileSize, screenSize, self.BOARD_SIZES.popleft(), self.DIFFICULTIES.popleft())
        
        self.monospaceFont = pygame.font.SysFont(FONT, 14)

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

    def draw(self, screen):
        difficulty = self.monospaceFont.render(self.gameBoard.getDifficulty().getName(), True, TEXT_COLOR)
        screen.blit(difficulty, ((self.screenSize[0] / 2) - (difficulty.get_width() / 2), self.screenSize[1] - (difficulty.get_height() + TEXT_MARGIN)))
        screen.blit(self.leftButton, self.difficultyLeftButtonPosition)
        screen.blit(self.difficultyText, self.difficultyTextPosition)
        screen.blit(self.rightButton, self.difficultyRightButtonPosition)

        tileBoardSize = self.monospaceFont.render("%d x %d" % self.gameBoard.getTileBoardSize(), True, TEXT_COLOR)
        screen.blit(self.leftButton, self.boardSizeLeftButtonPosition)
        screen.blit(self.boardSizeText, self.boardSizeTextPosition)
        screen.blit(self.rightButton, self.boardSizeRightButtonPosition)
        screen.blit(tileBoardSize, ((self.boardSizeTextPosition[0] + (self.boardSizeText.get_width() / 2)) - (tileBoardSize.get_width() / 2), self.boardSizeTextPosition[1] + TEXT_MARGIN + tileBoardSize.get_height()))

        if self.gameBoard.hasWon():
            screen.blit(self.winText, ((self.screenSize[0] / 2) - (self.winText.get_width() / 2), TEXT_MARGIN))
        else:
            flagsLeftText = self.monospaceFont.render("Flags left: %s" % (self.gameBoard.getFlagsLeft()), True, TEXT_COLOR)
            screen.blit(flagsLeftText, ((self.screenSize[0] / 2) - (flagsLeftText.get_width() / 2), TEXT_MARGIN))

        if self.gameBoard.isPlayable():
            screen.blit(self.howToPlayText, ((self.screenSize[0] / 2) - (self.howToPlayText.get_width() / 2), (self.howToPlayText.get_height() + (TEXT_MARGIN * 2))))
        else:
            screen.blit(self.playAgainText, ((self.screenSize[0] / 2) - (self.playAgainText.get_width() / 2), (self.playAgainText.get_height() + (TEXT_MARGIN * 2))))

        self.gameBoard.draw(screen)

    def processClick(self, event):
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

        if pressed1:
            leftButtonRect = self.getLeftButton().get_rect()
            rightButtonRect = self.getRightButton().get_rect()
            if leftButtonRect.move(self.getDifficultyLeftButtonPosition()).collidepoint(event.pos):
                self.difficultyRotateLeft()
            elif rightButtonRect.move(self.getDifficultyRightButtonPosition()).collidepoint(event.pos):
                self.difficultyRotateRight()
            elif leftButtonRect.move(self.getBoardSizeLeftButtonPosition()).collidepoint(event.pos):
                self.boardSizeRotateLeft()
            elif rightButtonRect.move(self.getBoardSizeRightButtonPosition()).collidepoint(event.pos):
                self.boardSizeRotateRight()

        self.gameBoard.processClick(event)

    def getGameBoard(self):
        return self.gameBoard

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
        self.DIFFICULTIES.appendleft(self.gameBoard.getDifficulty())
        self.gameBoard.setDifficulty(self.DIFFICULTIES.pop())

    def difficultyRotateRight(self):
        self.DIFFICULTIES.append(self.gameBoard.getDifficulty())
        self.gameBoard.setDifficulty(self.DIFFICULTIES.popleft())

    def getBoardSize(self):
        return self.tileBoardSize

    def getBoardSizeTextPosition(self):
        return self.boardSizeTextPosition

    def getBoardSizeLeftButtonPosition(self):
        return self.boardSizeLeftButtonPosition

    def getBoardSizeRightButtonPosition(self):
        return self.boardSizeRightButtonPosition

    def boardSizeRotateLeft(self):
        self.BOARD_SIZES.appendleft(self.gameBoard.getTileBoardSize())
        self.gameBoard.setTileBoardSize(self.BOARD_SIZES.pop())

    def boardSizeRotateRight(self):
        self.BOARD_SIZES.append(self.gameBoard.getTileBoardSize())
        self.gameBoard.setTileBoardSize(self.BOARD_SIZES.popleft())