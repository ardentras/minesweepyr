import pygame

pygame.font.init()

TILE_SIZE = 16
MONOSPACE_FONT = pygame.font.SysFont("Consolas", int(TILE_SIZE * .9), True)

class Tile(pygame.sprite.Sprite):
    def __init__(self, value = '', pos = (0, 0), color = (255, 255, 255), size = TILE_SIZE):
        MONOSPACE_FONT = pygame.font.SysFont("Consolas", int(size * .9), True)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((size, size))

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
            number = MONOSPACE_FONT.render(str(self.value), True, self.colorInverted)

            midwide = (self.size / 2) - (number.get_width() / 2)
            midhigh = (self.size / 2) - (number.get_height() / 2)

            self.image.fill(self.color)
            self.image.blit(number, (midwide,midhigh))
        elif self.uncovered:
            self.image.fill(self.colorInverted)
        elif self.flagged:
            number = MONOSPACE_FONT.render(str("F"), True, self.colorInverted)

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