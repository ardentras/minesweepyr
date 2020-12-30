###########################################################
# Filename: tiles.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#
# tile classes for numbers and mines
#

import pygame
import colors

pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont("Courier New", 16, True)
MINE = 9

class Tile(pygame.sprite.Sprite):
    def __init__(self, value = 0, pos = (0, 0), color = colors.WHITE, size = 16, font=DEFAULT_FONT):
        pygame.sprite.Sprite.__init__(self)

        self.borderScale = .95
        self.image = pygame.Surface((size, size))
        self.tile = pygame.Surface((size * self.borderScale, size * self.borderScale))

        self.font = font
        self.size = size
        self.color = color
        self.colorInverted = (255-self.color[0],255-self.color[1],255-self.color[2])
        self.colorDimmed = (abs(self.color[0] - 32),abs(self.color[1] - 32),abs(self.color[2] - 32))
        
        self.uncovered = False
        self.flagged = False
        self.value = value

        self.rect = (pos[0] * self.size, pos[1] * self.size)

        self.redraw()

    def redraw(self):
        return

    def draw(self, value, bkg=None, border=colors.LTGRAY):
        if bkg == None:
            bkg = self.colorDimmed
            
        number = self.font.render(str(value), True, self.colorInverted)

        numMidwide = (self.size / 2) - (number.get_width() / 2)
        numMidhigh = (self.size / 2) - (number.get_height() / 2)
        tileMidwide = (self.size / 2) - ((self.size * self.borderScale) / 2)
        tileMidhigh = (self.size / 2) - ((self.size * self.borderScale) / 2)

        self.tile.fill(bkg)
        self.image.fill(border)
        
        self.image.blit(self.tile, (tileMidwide,tileMidhigh))
        self.image.blit(number, (numMidwide,numMidhigh))

    def setUncovered(self, uncovered):
        if not self.flagged:
            self.uncovered = uncovered
            self.redraw()

    def isUncovered(self):
        return self.uncovered

    def setFlagged(self, flagged):
        if not self.uncovered:
            self.flagged = flagged
            self.redraw()

    def isFlagged(self):
        return self.flagged

    def getValue(self):
        return int(self.value) if self.value != 'X' else 9

class NumberTile(Tile):
    def __init__(self, value = 0, pos = (0, 0), color = colors.WHITE, size = 16, font=DEFAULT_FONT):
        super().__init__(value, pos, color, size, font)

    def redraw(self):
        if self.uncovered:
            if self.value > 0:
                self.draw(self.value)
            else:
                self.image.fill(self.colorDimmed)
        elif self.flagged:
            self.draw("F", self.color)
        else:
            self.draw("", self.color)

class MineTile(Tile):
    def __init__(self, pos = (0, 0), color = colors.WHITE, size = 16, font=DEFAULT_FONT):
        super().__init__(MINE, pos, color, size, font)

    def redraw(self):
        if self.uncovered:
            self.draw("X", (219, 55, 0))
        elif self.flagged:
            self.draw("F", self.color)
        else:
            self.draw("", self.color)
