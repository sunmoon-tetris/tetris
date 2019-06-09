import sys
import pygame
from pygame.locals import *
import cv2
import random

def selectMino(minoList):
    global cnt, mino_choice
    if cnt > 6:
        cnt -= 7
    if cnt == 0:
        minoList[0] = [i for i in minoList[1]]
        random.shuffle(minoList[1])
    mino_choice = minoList[0][cnt]
    cnt += 1
    return mino_choice

def loadBoard():
    for x in range(1, 11):
        for y in range(1, 21):
            for i in range(16):
                img_y = i
                img_x = 0
                if i == 15:
                    img_y == 0
                    img_x = size
                elif i > 8:
                    img_y -= 7
                    img_x = size
                if board[x][y] == i:
                    screen.blit(img, ((x - 1) * size, (20 - y) * size),
                                (img_x, img_y * size, size, size))

def putMino(mino, action = False):
    if board[mino[0]][mino[1]] != 0:
        return False
    if action:
        board[mino[0]][mino[1]] = mino[2]
    for i in range(3):
        dx = minos[mino[2]][1][i][0]
        dy = minos[mino[2]][1][i][1]
        r = mino[3] % minos[mino[2]][0]
        for j in range(r):
            dx, dy = dy, -dx
        if board[mino[0] + dx][mino[1] + dy] != 0:
            return False
        if action:
            board[mino[0] + dx][mino[1] + dy] = mino[2]
    if not action:
        putMino(mino, True)
    return True

def deleteMino(mino):
    board[mino[0]][mino[1]] = 0
    for i in range(3):
        dx = minos[mino[2]][1][i][0]
        dy = minos[mino[2]][1][i][1]
        r = mino[3] % minos[mino[2]][0]
        for j in range(r):
            dx, dy = dy, -dx
        board[mino[0] + dx][mino[1] + dy] = 0

def superDrop():
    global block, mino
    block = [i for i in mino]
    block[2] += 7
    for x in range(1, 11):
        for y in range(1, 21):
            if board[x][y] > 7:
                board[x][y] = 0
    while True:
        block[1] -= 1
        if not putMino(block):
            block[1] += 1
            putMino(block)
            break

def processInput():
    global mino, fin, con
    ret = False
    n = [i for i in mino]
    if event.key == K_ESCAPE:
        fin = True
        con = False
    elif event.key == K_UP:
        n[3] += 1
    elif event.key == K_DOWN:
        ret = True
    elif event.key == K_LEFT:
        n[0] -= 1
    elif event.key == K_RIGHT:
        n[0] += 1
    if n[0] != mino[0] or n[1] != mino[1] or n[3] != mino[3]:
        deleteMino(mino)
        if putMino(n):
            mino = [i for i in n]
        else:
            putMino(mino)
    return ret

def minoDown():
    global mino
    deleteMino(mino)
    mino[1] -= 1
    if not putMino(mino):
        mino[1] += 1
        putMino(mino)
        deleteLine()
        mino = [5, 21, 0, 0]
        mino[2] = selectMino(minoList)
        if not putMino(mino):
            gameOver()

def gameOver():
    global con, board
    for x in range(1, 11):
        for y in range(1, 21):
            if board[x][y] != 0:
                board[x][y] = 5
    con = False

def deleteLine():
    global pawer
    y = 1
    while y < 21:
        flag = True
        for x in range(1, 11):
            if board[x][y] == 0:
                flag = False
        if flag:
            for j in range(y, 21):
                for i in range(1, 11):
                    board[i][j] = board[i][j + 1]
            pawer += 1
            y -= 1
        y += 1

img = pygame.image.load("img.png")
size = 24
board = [[0 for i in range(25)] for i in range(12)]
for x in range(len(board)):
    for y in range(len(board[x])):
        if x == 0 or x == 11 or y == 0:
            board[x][y] = 1
minos = [
    [1, [[0, 0], [0, 0], [0, 0]]],     ## null
    [2, [[0, -1], [0, 1], [0, 2]]],    ## I mino
    [4, [[0, -1], [0, 1], [1, 1]]],    ## L mino
    [4, [[0, -1], [0, 1], [-1, 1]]],   ## J mino
    [2, [[0, -1], [1, 0], [1, 1]]],    ## S mino
    [2, [[0, -1], [-1, 0], [-1, 1]]],  ## Z mino
    [1, [[0, 1], [1, 0], [1, 1]]],     ## O mino
    [4, [[0, -1], [1, 0], [-1, 0]]],   ## T mino
    [2, [[0, -1], [0, 1], [0, 2]]],    ## I mino for superDrop
    [4, [[0, -1], [0, 1], [1, 1]]],    ## L mino for superDrop
    [4, [[0, -1], [0, 1], [-1, 1]]],   ## J mino for superDrop
    [2, [[0, -1], [1, 0], [1, 1]]],    ## S mino for superDrop
    [2, [[0, -1], [-1, 0], [-1, 1]]],  ## Z mino for superDrop
    [1, [[0, 1], [1, 0], [1, 1]]],     ## O mino for superDrop
    [4, [[0, -1], [1, 0], [-1, 0]]]    ## T mino for superDrop
    ]
mino = [5, 21, 0, 0]                   ## x, y, type, rotate
minoList = [[1, 2, 3, 4, 5, 6, 7],
            [1, 2, 3, 4, 5, 6, 7]]
random.shuffle(minoList[0])
random.shuffle(minoList[1])
cnt = 0
time = 0
pawer = 0
fin = False
con = True
nxt = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((size * 10, size * 20))
pygame.display.set_caption("Tetris")
pygame.display.update()

while not fin:
    if con:
        clock.tick(30)
        time += 1
        if nxt:
            mino[2] = selectMino(minoList)
            nxt = False
        putMino(mino)
        if time % 10 == 0:
            minoDown()
    for event in pygame.event.get():
        if event.type == QUIT:
            fin = True
            con = False
        if event.type == KEYDOWN:
            if(processInput()):
                time = -1
    superDrop()
    loadBoard()
    pygame.display.update()

pygame.quit()
sys.exit()
