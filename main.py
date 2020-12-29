import sys, pygame
import board, tiles

pygame.init()

running = True

size = width, height = 640, 480
boardSize = (128 * 2, 128 * 3)

black = 0, 0, 0

screen = pygame.display.set_mode(size)

gameBoard = pygame.Surface(boardSize)

tileGroup = board.fillBoard(pygame.sprite.Group(), boardSize, 16)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    tileGroup.draw(gameBoard)
    screen.blit(gameBoard, ((width / 2) - (gameBoard.get_width() / 2), (height / 2) - (gameBoard.get_height() / 2)))
    
    pygame.display.flip()


pygame.quit()
sys.exit()