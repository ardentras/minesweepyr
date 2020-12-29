import pygame
import tiles
import random

INV_PROB = 2
MINE = 9

def fillBoard(tileGroup, space, size, minesMax = 30):
    mineProb = 0.05
    random.seed()

    w = int(space[0] / size)
    if space[0] % size != 0: w = w - 1
    h = int(space[1] / size)
    if space[1] % size != 0: h = h - 1

    mineCount = 0
    mineMatrix = [[random.random() for e in range(h)] for e in range(w)]
    board = [[0 for e in range(h)] for e in range(w)]

    while mineCount < minesMax:
        for x in range(w):
            for y in range(h):
                if mineMatrix[x][y] < mineProb and mineCount < minesMax:
                    mineCount = mineCount + 1
                    mineMatrix[x][y] = INV_PROB
                    board[x][y] = MINE

                    for x1 in range(x - 1 if x - 1 > 0 else 0, x + 2 if x + 2 < w else w):
                        for y1 in range(y - 1 if y - 1 > 0 else 0, y + 2 if y + 2 < h else h):
                            if board[x1][y1] < 8:
                                board[x1][y1] = board[x1][y1] + 1

                if mineCount >= minesMax:
                    break
            if mineCount >= minesMax:
                break
        if mineCount >= minesMax:
            break
        
        mineProb = mineProb + 0.05
        
    for x in range(w):
        for y in range(h):
            if board[x][y] == MINE:
                tileGroup.add(tiles.Tile(value="X", pos=(x, y)))
            else:
                tileGroup.add(tiles.Tile(value=str(board[x][y]), pos=(x, y)))
            
    return tileGroup