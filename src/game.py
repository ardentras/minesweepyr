###########################################################
# Filename: game.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/31/2020
#
# Visual elements outside of the tile board
#

import pygame
import board
import colors as c
import json
from collections import deque

FONT = "Courier New"

SETTINGS_FILENAME = 'settings.json'
TEXT_MARGIN = 5

class Theme():
    def __init__(self, themeJSON=None):
        self.name = "Default"

        self.textFont = pygame.font.SysFont("Courier New", 14, False)
        self.tileFont = pygame.font.SysFont("Courier New", 16, False)

        self.textColor = c.WHITE
        self.backgroundColor = c.GRAY
        self.boardColor = c.BLACK
        self.tileColor = c.WHITE
        self.tileCoverColor = c.LGRAY
        self.tileBorderColor = c.LGRAY
        self.mineColor = c.RED

        if themeJSON:
            if "name" in themeJSON:
                self.name = themeJSON["name"]

            if "textFont" in themeJSON:
                self.textFont = self.processFont(themeJSON["textFont"])
            if "tileFont" in themeJSON:
                self.tileFont = self.processFont(themeJSON["tileFont"])

            if "colors" in themeJSON:
                colors = themeJSON["colors"]
                
                if "text" in colors:
                    self.textColor = self.hexStringToRGB(colors["text"])
                if "background" in colors:
                    self.backgroundColor = self.hexStringToRGB(colors["background"])
                if "board" in colors:
                    self.boardColor = self.hexStringToRGB(colors["board"])
                if "tile" in colors:
                    self.tileColor = self.hexStringToRGB(colors["tile"])
                if "tileCover" in colors:
                    self.tileCoverColor = self.hexStringToRGB(colors["tileCover"])
                if "tileBorder" in colors:
                    self.tileBorderColor = self.hexStringToRGB(colors["tileBorder"])
                if "mine" in colors:
                    self.mineColor = self.hexStringToRGB(colors["mine"])

        self.tileColorInverted = (255-self.tileColor[0],255-self.tileColor[1],255-self.tileColor[2])

    def processFont(self, f):
        return pygame.font.SysFont(f["name"], f["size"] if "size" in f else 16, f["bold"] if "bold" in f else False)

    def hexStringToRGB(self, hex):
        return (int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))

class Difficulty():
    def __init__(self, name, modifier):
        self.name = name
        self.modifier = modifier
    
    def getName(self):
        return self.name
    
    def getModifier(self):
        return self.modifier

class MenuOption():
    def __init__(self, name, options, theme, pos):
        self.theme = theme

        self.centerPosition = pos
        self.options = options
        self.currentOption = self.options.popleft()

        self.text = self.theme.textFont.render(name, True, self.theme.textColor)
        self.leftButton = self.theme.textFont.render("<", True, self.theme.textColor)
        self.rightButton = self.theme.textFont.render(">", True, self.theme.textColor)

        self.textPosition = (self.centerPosition[0] - (self.text.get_width() / 2), self.centerPosition[1])
        self.leftButtonPosition = (self.textPosition[0] - self.leftButton.get_width() - TEXT_MARGIN, self.textPosition[1])
        self.rightButtonPosition = (self.textPosition[0] + self.text.get_width() + TEXT_MARGIN, self.textPosition[1])

    def draw(self, screen, currentOptionFormat):
        optionText = self.theme.textFont.render(currentOptionFormat(self.currentOption), True, self.theme.textColor)
        optionTextPosition = (self.centerPosition[0] - (optionText.get_width() / 2), self.centerPosition[1] + optionText.get_height() + TEXT_MARGIN)

        screen.blit(self.leftButton, self.leftButtonPosition)
        screen.blit(self.text, self.textPosition)
        screen.blit(self.rightButton, self.rightButtonPosition)
        screen.blit(optionText, optionTextPosition)

    def processClick(self, event):
        pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()

        if pressed1:
            leftButtonRect = self.leftButton.get_rect()
            rightButtonRect = self.rightButton.get_rect()
            if leftButtonRect.move(self.leftButtonPosition).collidepoint(event.pos):
                self.rotateLeft()
            elif rightButtonRect.move(self.rightButtonPosition).collidepoint(event.pos):
                self.rotateRight()
            else:
                return False
            
            return True

        return False

    def rotateLeft(self):
        self.options.appendleft(self.currentOption)
        self.currentOption = self.options.pop()

    def rotateRight(self):
        self.options.append(self.currentOption)
        self.currentOption = self.options.popleft()

    def getCurrentOption(self):
        return self.currentOption

class Game():
    def __init__(self, tileSize, screenSize):
        self.screenSize = screenSize
        
        settingsText = ""
        with open(SETTINGS_FILENAME, "r") as inFile:
            settingsText = inFile.read()
            
        settings = json.loads(settingsText)

        self.THEMES = deque()
        self.THEMES.append(Theme())
        if "themes" in settings:
            for theme in settings["themes"]:
                self.THEMES.append(Theme(theme))
        self.theme = self.THEMES.popleft()
        
        DIFFICULTIES = deque()
        for difficulty in settings['difficulties']:
            DIFFICULTIES.append(Difficulty(difficulty['name'], difficulty['modifier']))

        BOARD_SIZES = deque()
        for boardSize in settings['boardSizes']:
            BOARD_SIZES.append((boardSize[0], boardSize[1]))

        difficultyOptionPosition = (self.screenSize[0] / 2, self.screenSize[1] - ((self.theme.textFont.get_height() + TEXT_MARGIN) * 2))
        self.difficultyOption = MenuOption("DIFFICULTY", DIFFICULTIES, self.theme, difficultyOptionPosition)

        boardSizeOptionPosition = (self.screenSize[0] / 4, self.screenSize[1] - ((self.theme.textFont.get_height() + TEXT_MARGIN) * 2))
        self.boardSizeOption = MenuOption("BOARD SIZE", BOARD_SIZES, self.theme, boardSizeOptionPosition)

        self.gameBoard = board.Board(tileSize, screenSize, self.boardSizeOption.getCurrentOption(), self.difficultyOption.getCurrentOption(), self.theme)
        
        self.winText = self.theme.textFont.render("Congratulations, you won!", True, self.theme.textColor)
        self.howToPlayText = self.theme.textFont.render("Left click to reveal. Right click to flag.", True, self.theme.textColor)
        self.playAgainText = self.theme.textFont.render("Click anywhere on the board to start.", True, self.theme.textColor)

    def draw(self, screen):
        screen.fill(self.theme.backgroundColor)

        self.difficultyOption.draw(screen, (lambda e: e.getName()))
        self.boardSizeOption.draw(screen, (lambda e: "%d x %d" % e))

        if self.gameBoard.hasWon():
            screen.blit(self.winText, ((self.screenSize[0] / 2) - (self.winText.get_width() / 2), TEXT_MARGIN))
        else:
            flagsLeftText = self.theme.textFont.render("Flags left: %s" % (self.gameBoard.getFlagsLeft()), True, self.theme.textColor)
            screen.blit(flagsLeftText, ((self.screenSize[0] / 2) - (flagsLeftText.get_width() / 2), TEXT_MARGIN))

        if self.gameBoard.isPlayable():
            screen.blit(self.howToPlayText, ((self.screenSize[0] / 2) - (self.howToPlayText.get_width() / 2), (self.howToPlayText.get_height() + (TEXT_MARGIN * 2))))
        else:
            screen.blit(self.playAgainText, ((self.screenSize[0] / 2) - (self.playAgainText.get_width() / 2), (self.playAgainText.get_height() + (TEXT_MARGIN * 2))))

        self.gameBoard.draw(screen)

    def processClick(self, event):
        if self.difficultyOption.processClick(event):
            self.gameBoard.setDifficulty(self.difficultyOption.getCurrentOption())
        if self.boardSizeOption.processClick(event):
            self.gameBoard.setTileBoardSize(self.boardSizeOption.getCurrentOption())
        self.gameBoard.processClick(event)

    def getGameBoard(self):
        return self.gameBoard