import pygame

pygame.font.init()

TILE_SIZE = 16
MONOSPACE_FONT = pygame.font.SysFont("Consolas", int(TILE_SIZE * .9), True)


class Tile(pygame.sprite.Sprite):
    def __init__(self, value = '', pos = (0, 0), color = (255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))

        self.size = TILE_SIZE
        self.color = color
        self.colorInverted = (255-self.color[0],255-self.color[1],255-self.color[2])
        # self.uncovered = False
        self.uncovered = True
        self.setValue(value)

        self.rect = (pos[0] * self.size, pos[1] * self.size)
    
    def setValue(self, value):
        if self.uncovered and value != '0':
            number = MONOSPACE_FONT.render(str(value), True, self.colorInverted)

            midwide = (self.size / 2) - (number.get_width() / 2)
            midhigh = (self.size / 2) - (number.get_height() / 2)

            self.image.fill(self.color)
            self.image.blit(number, (midwide,midhigh))
        else:
            self.image.fill(self.color)
