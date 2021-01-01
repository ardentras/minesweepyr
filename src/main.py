###########################################################
# Filename: main.py
# Author: Shaun Rasmusen <shaunrasmusen@gmail.com>
# Last Modified: 12/31/2020
#
# entrypoint and main loop
#

import sys, pygame
import colors, game

pygame.init()

pygame.display.set_caption("Minesweepyr")
screen = pygame.display.set_mode((640, 480))

game = game.Game(16, screen.get_size())
game.draw(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.processClick(event)
                
    screen.fill(colors.GRAY)
    game.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()