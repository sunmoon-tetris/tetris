##  Player class
##
##  tetris를 부는 프로그램.
##
##  varsion: 2019/07/05
##  author: Katsutoshi Eda

from Tetris import *
from Player import *
import sys
import pygame
from pygame.locals import *
import random

class Game:
    def __init__(self):
        self.tetris = []
        self.tetris.append(Tetris())
        self.tetris.append(Tetris())
        self.player = []
        self.player.append(Player())
        self.player.append(Player())
##      mino는 7개의 종류가 있고 7개의 순서를 random으로 저장하고 list를 만든다.
        self.minoList = [[i + 1 for i in range(7)] for j in range(2)]
        for i in range(2):
            random.shuffle(self.minoList[i])
            self.tetris[i].setMinoList(self.minoList)
            self.tetris[i].mino[2] = self.tetris[i].selectMino()
            self.tetris[i].block[2] = self.tetris[i].mino[2] + 7
        pygame.init()
        pygame.display.set_caption("Tetris")
        pygame.mixer.music.load("sound_effect/BGM2.wav")
        pygame.mixer.music.play(-1)
        self.size1 = 24
        self.size2 = 15
        self.size3 = 20
        self.img1 = pygame.image.load("img.png")
        self.img2 = pygame.transform.scale(self.img1, (self.size2 * 2, self.size2 * 8))
        self.img3 = pygame.transform.scale(self.img1, (self.size3 * 2, self.size3 * 8))
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.size1 * 40 + 40, self.size1 * 20 + 50))
        self.clear = pygame.mixer.Sound("sound_effect/clear.wav")
        self.line = pygame.mixer.Sound("sound_effect/line.wav")
        self.damage = pygame.mixer.Sound("sound_effect/damage.wav")
        self.allClear = pygame.mixer.Sound("sound_effect/allClear.wav")
        self.fall = pygame.mixer.Sound("sound_effect/fall.wav")

    def main(self):
        fin = False
        while not fin:
            self.clock.tick(30)
            self.addMonoList()
            fin = self.updateTetris()
            self.putBlock()
            self.drawBoard()

    def addMonoList(self):
        n = self.tetris[0].cnt
        if n < self.tetris[1].cnt: n = self.tetris[1].cnt
        if n // 7 >= len(self.minoList) - 1:
            temp = [i + 1 for i in range(7)]
            random.shuffle(temp)
            self.minoList.append(temp)
            for i in range(2):
                self.tetris[i].setMinoList(self.minoList)

    def getCommand(self, player, tetris):
        ret = False
        key = -1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP: key = 0
                elif event.key == K_r: key = 1
                elif event.key == K_DOWN: key = 2
                elif event.key == K_LEFT: key = 3
                elif event.key == K_RIGHT: key = 4
                elif event.key == K_f: key = 5
                elif event.key == K_q: key = 6
##        key = player.answer(tetris.getLists(), tetris.mino)
        if key == 2 or key == 6:
            ret = True
        tetris.processInput(key)
        return ret

    def updateTetris(self):
        fin = False
        for i in range(1, 3):
            ret = self.getCommand(self.player[i - 1], self.tetris[i - 1])
            se = self.tetris[i - 1].countTime(ret, self.tetris[2 - i].pawer)
            if se == 1: self.fall.play()
            elif se == 2: self.line.play()
            elif se == 3: self.allClear.play()
            elif se == 4: self.damage.play()
            elif se == 5:
                self.clear.play()
                pygame.mixer.music.pause()
                fin = True
        return fin

    def putBlock(self):
        for i in range(2):
            self.tetris[i].hardDrop()

    def drawBoard(self):
        self.screen.fill((128, 192, 255))
        lists = []
        lists.append(self.tetris[0].getLists())
        lists.append(self.tetris[1].getLists())
        for n in range(2):
            for x in range(1, 11):
                for y in range(1, 21):
                    for i in range(16):
                        img_y = i
                        img_x = 0
                        if i == 15:
                            img_y = 0
                            img_x = self.size1
                        elif i > 7:
                            img_y -= 7
                            img_x = self.size1
                        if lists[n][0][x][y] == i: self.screen.blit(self.img1, ((x + 4 + (n * 20)) * self.size1 + 10 + (n * 20), (20 - y) * self.size1 + 10),
                                                                    (img_x, img_y * self.size1, self.size1, self.size1))

            for x in range(5):
                for y in range(5):
                    for i in range(16):
                        img_y = i
                        img_x = 0
                        if i == 15:
                            img_y = 0
                            img_x = self.size2
                        elif i > 7:
                            img_y -= 7
                            img_x = self.size2
                        if lists[n][1][x][y] == i: self.screen.blit(self.img2, (x * self.size2 + 45 + (n * 20) * self.size1 + (n * 20), y * self.size2 + 10),
                                                                    (img_x, img_y * self.size2, self.size2, self.size2))

            for m in range(5):
                for x in range(5):
                    for y in range(5):
                        for i in range(16):
                            img_y = i
                            img_x = 0
                            if i == 15:
                                img_y = 0
                                img_x = self.size2
                            elif i > 7:
                                img_y -= 7
                                img_x = self.size2
                            if lists[n][2][m][x][y] == i: self.screen.blit(self.img2, ((15 + (n * 20)) * self.size1 + x * self.size2 + 15 + (n * 20), (m * 5 + y) * self.size2 + 12),
                                                                           (img_x, img_y * self.size2, self.size2, self.size2))
            lists[n][3].reverse()
            for i in range(20):
                if len(lists[n][3]) > i:
                    if lists[n][3][i] > 5: self.screen.blit(self.img3, ((n * 20) * self.size1 + 100 + (n * 20), (19 - i) * self.size3 + 90),
                                                            (0, 6 * self.size3, self.size3, self.size3))
                    else: self.screen.blit(self.img3, ((n * 20) * self.size1 + 100 + (n * 20), (19 - i) * self.size3 + 90),
                                      (0, 4 * self.size3, self.size3, self.size3))
                else: self.screen.blit(self.img3, ((n * 20) * self.size1 + 100 + (n * 20), (19 - i) * self.size3 + 90),
                                  (self.size3, 0 * self.size3, self.size3, self.size3))
            lists[n][3].reverse()
        pygame.display.update()

    def end(self, index):
        fin = False
        while not fin:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_SPACE and index != 2:
                        fin = True

for i in range(3):
    game = Game()
    game.main()
    game.end(i)
