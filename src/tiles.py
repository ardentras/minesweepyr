###########################################################
# Filename: tiles.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/31/2020
#
# tile classes for numbers and mines
#

import pygame
import colors

pygame.font.init()

MINE = 9

class Tile(pygame.sprite.Sprite):
    def __init__(self, value, pos, theme, size = 16):
        pygame.sprite.Sprite.__init__(self)

        self.borderScale = .95
        self.image = pygame.Surface((size, size))
        self.tile = pygame.Surface((size * self.borderScale, size * self.borderScale))

        self.size = size
        self.theme = theme
        
        self.uncovered = False
        self.flagged = False
        self.value = value

        self.rect = (pos[0] * self.size, pos[1] * self.size)

        self.redraw()

    def redraw(self):
        return

    def draw(self, value, color):
        number = self.theme.tileFont.render(str(value), True, (255-color[0],255-color[1],255-color[2]))

        numMidwide = (self.size / 2) - (number.get_width() / 2)
        numMidhigh = (self.size / 2) - (number.get_height() / 2)
        tileMidwide = (self.size / 2) - ((self.size * self.borderScale) / 2)
        tileMidhigh = (self.size / 2) - ((self.size * self.borderScale) / 2)

        self.tile.fill(color)
        self.image.fill((abs(color[0]-32),abs(color[1]-32),abs(color[2]-32)))
        
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

    def setTheme(self, theme):
        self.theme = theme

class NumberTile(Tile):
    def __init__(self, value, pos, theme, size = 16):
        super().__init__(value, pos, theme, size)

    def redraw(self):
        if self.uncovered:
            if self.value > 0:
                self.draw(self.value, self.theme.tileColor)
            else:
                self.image.fill(self.theme.tileColor)
        elif self.flagged:
            self.draw("F", self.theme.tileCoverColor)
        else:
            self.draw("", self.theme.tileCoverColor)

class MineTile(Tile):
    def __init__(self, pos, theme, size = 16):
        super().__init__(MINE, pos, theme, size)

    def redraw(self):
        if self.uncovered:
            self.draw("X", self.theme.mineColor)
        elif self.flagged:
            self.draw("F", self.theme.tileCoverColor)
        else:
            self.draw("", self.theme.tileCoverColor)
