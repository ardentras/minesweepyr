###########################################################
# Filename: tiles.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#

import pygame

pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont("Consolas", 16, True)
MINE = 9

class Tile(pygame.sprite.Sprite):
    def __init__(self, value = 0, pos = (0, 0), color = (255, 255, 255), size = 16, font=DEFAULT_FONT):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((size, size))

        self.font = font
        self.size = size
        self.color = color
        self.colorInverted = (255-self.color[0],255-self.color[1],255-self.color[2])
        
        self.uncovered = False
        self.flagged = False
        self.value = value

        self.rect = (pos[0] * self.size, pos[1] * self.size)

        self.redraw()

    def redraw(self):
        return

    def draw(self, value):
        number = self.font.render(str(value), True, self.colorInverted)

        midwide = (self.size / 2) - (number.get_width() / 2)
        midhigh = (self.size / 2) - (number.get_height() / 2)

        self.image.fill(self.color)
        self.image.blit(number, (midwide,midhigh))

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
    def __init__(self, value = 0, pos = (0, 0), color = (255, 255, 255), size = 16, font=DEFAULT_FONT):
        super().__init__(value, pos, color, size, font)

    def redraw(self):
        if self.uncovered:
            if self.value > 0:
                self.draw(self.value)
            else:
                self.image.fill(self.colorInverted)
        elif self.flagged:
            self.draw("F")
        else:
            self.image.fill(self.color)

class MineTile(Tile):
    def __init__(self, pos = (0, 0), color = (255, 255, 255), size = 16, font=DEFAULT_FONT):
        super().__init__(MINE, pos, color, size, font)

    def redraw(self):
        if self.uncovered:
            self.draw("X")
        elif self.flagged:
            self.draw("F")
        else:
            self.image.fill(self.color)
