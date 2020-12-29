###########################################################
# Filename: tiles.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/29/2020
#

import pygame

pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont("Consolas", 16, True)

class Tile(pygame.sprite.Sprite):
    def __init__(self, value = '', pos = (0, 0), color = (255, 255, 255), size = 16, font=DEFAULT_FONT):
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
        if self.uncovered and self.value != '0':
            number = self.font.render(str(self.value), True, self.colorInverted)

            midwide = (self.size / 2) - (number.get_width() / 2)
            midhigh = (self.size / 2) - (number.get_height() / 2)

            self.image.fill(self.color)
            self.image.blit(number, (midwide,midhigh))
        elif self.uncovered:
            self.image.fill(self.colorInverted)
        elif self.flagged:
            number = self.font.render(str("F"), True, self.colorInverted)

            midwide = (self.size / 2) - (number.get_width() / 2)
            midhigh = (self.size / 2) - (number.get_height() / 2)

            self.image.fill(self.color)
            self.image.blit(number, (midwide,midhigh))
        else:
            self.image.fill(self.color)

    def setUncovered(self, uncovered):
        self.uncovered = uncovered
        self.redraw()

    def getUncovered(self):
        return self.uncovered

    def setFlagged(self, flagged):
        self.flagged = flagged
        self.redraw()

    def getFlagged(self):
        return self.flagged

    def getValue(self):
        return int(self.value) if self.value != 'X' else 9