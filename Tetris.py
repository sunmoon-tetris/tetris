##  Tetris class
##
##  tetris를 간리하는 프로그램. Player class에서 행동을 받아 처리하고 list로 저장한다.
##
##  varsion: 2019/07/05
##  author: Katsutoshi Eda

import random

class Tetris:
    def __init__(self):
##      block(mino)의 돌 수 있는 개수, 모양 설정.
        self.minos = [                      ## 종류번호: block이름
            [1, [0, 0], [0, 0], [0, 0]],    ## 0:   null
            [2, [0, -1], [0, 1], [0, 2]],   ## 1:   I mino
            [4, [0, -1], [0, 1], [1, 1]],   ## 2:   J mino
            [4, [0, -1], [0, 1], [-1, 1]],  ## 3:   L mino
            [2, [0, -1], [1, 0], [1, 1]],   ## 4:   Z mino
            [2, [0, -1], [-1, 0], [-1, 1]], ## 5:   S mino
            [1, [0, 1], [1, 0], [1, 1]],    ## 6:   O mino
            [4, [0, -1], [1, 0], [-1, 0]],  ## 7:   T mino
            [2, [0, -1], [0, 1], [0, 2]],   ## 8:   I mino of hard drop
            [4, [0, -1], [0, 1], [1, 1]],   ## 9:   J mino of hard drop
            [4, [0, -1], [0, 1], [-1, 1]],  ## 10:  L mino of hard drop
            [2, [0, -1], [1, 0], [1, 1]],   ## 11:  Z mino of hard drop
            [2, [0, -1], [-1, 0], [-1, 1]], ## 12:  S mino of hard drop
            [1, [0, 1], [1, 0], [1, 1]],    ## 13:  O mino of hard drop
            [4, [0, -1], [1, 0], [-1, 0]]   ## 14:  T mino of hard drop
            ]                               ## 15:  disturbing block
##      x: 12, y: 45로 구성. block이 없을 때 0. 벽은 1. block이 있을 때는 block의 종류.
        self.board = [[0 for i in range(45)] for j in range(12)]
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if x == 0 or x == 11 or y == 0: self.board[x][y] = 1
##      x: 5, y: 5로 구성. block이 없을 때 15. block이 있을 때는 board_hold[2][2]를 중심으로 저장. 숫자는 block의 종류.
        self.board_hold = [[15 for i in range(5)] for j in range(5)]
##      개수: 5, x: 5, y: 5로 구성. nexts[n][2][2]를 중심으로 저장. 숫자는 block의 종류.
        self.nexts = [[[15 for i in range(5)] for j in range(5)] for k in range(5)]
##      상대방의공격을 저장 되어 있는 list. 15부터 시작하고 전전히 내린다. 0이 되면 disturbing block이 생긴다. 공격이 없을 때는 list의 length는 0.
        self.attack = []
##      mino의 순서를 저장 되어 있는 list를 받기위한 변수 선언.
        self.minoList = None
##      mino를 몇개 내는지를 count하는 변수.
        self.cnt = 0
##      자신의 공격
        self.pawer = 0
##      attack list의 있는 공격이 0이 되었을때 몇개 있는지를 새는 변수.
        self.wall = 0
##      Game class에서 tick를 받아 block이 내릴 때를 반단하는 변수.
        self.time = 0
##      block를 지웠을 때 연속으로 몇번 지웠는지를 새는 변수.
        self.chain = 0
##      hold는 한번 하면 block을 다내릴 때까지 하지 못한다. hold할 수 있는지 없는지를 반단하는 변수. 
        self.canHold = True
##      (back to back) 연속으로 tetris(4줄 지우기)했는지를 반단하는 변수.
        self.btb = False
##      mino list는 x, y, 종류 회전으로 구성.
        self.mino = [5, 21, 0, 0]
##      hard drop 예측block
        self.block = [i for i in self.mino]
##      hold 하고 있는 block를 저장하는 변수. 없을 때는 null(None)
        self.hold = None

##  mino의 종류를 구하는 method. return값은 int(block의 종류)
    def selectMino(self):
        for n in range(5):
            for x in range(5):
                for y in range(5): self.nexts[n][x][y] = 15
            nxt = self.cnt + n + 1
            self.nexts[n][2][2] = self.minoList[nxt // 7][nxt % 7]
            for i in range(3):
                dx = self.minos[self.minoList[nxt // 7][nxt % 7]][i + 1][0]
                dy = self.minos[self.minoList[nxt // 7][nxt % 7]][i + 1][1]
                self.nexts[n][2 + dx][2 + dy] = self.minoList[nxt // 7][nxt % 7]
        for j in range(5):
            for k in range(5): self.nexts[j][k].reverse()
        minoChoice = self.minoList[self.cnt // 7][self.cnt % 7]
        self.cnt += 1
        return minoChoice

##  mino가 둘 수 있는지 반단하는 method. return값은 boolean(True일 때 board에 저장)
    def putMino(self, mino, action = False):
        if self.board[mino[0]][mino[1]] != 0 and self.board[mino[0]][mino[1]] < 8\
           or self.board[mino[0]][mino[1]] == 15: return False
        if action: self.board[mino[0]][mino[1]] = mino[2]
        for i in range(3):
            dx = self.minos[mino[2]][i + 1][0]
            dy = self.minos[mino[2]][i + 1][1]
            r = mino[3] % self.minos[mino[2]][0]
            for j in range(r): dx, dy = dy, -dx
            if self.board[mino[0] + dx][mino[1] + dy] != 0 and self.board[mino[0] + dx][mino[1] + dy] < 8\
               or self.board[mino[0] + dx][mino[1] + dy] == 15: return False
            if action: self.board[mino[0] + dx][mino[1] + dy] = mino[2]
        if not action: self.putMino(mino, True)
        return True

##  block(mino)의 정보를 받아 board에 있는 block(mino)를 삭제하는 method.
    def deleteMino(self, mino):
        self.board[mino[0]][mino[1]] = 0
        for i in range(3):
            dx = self.minos[mino[2]][i + 1][0]
            dy = self.minos[mino[2]][i + 1][1]
            r = mino[3] % self.minos[mino[2]][0]
            for j in range(r): dx, dy = dy, -dx
            self.board[mino[0] + dx][mino[1] + dy] = 0

##  hard drop 예측block를 만드는 method.
    def hardDrop(self):
        temp = [[] for i in range(4)]
        for i in range(3):
            dx = self.minos[self.mino[2]][i + 1][0]
            dy = self.minos[self.mino[2]][i + 1][1]
            r = self.mino[3] % self.minos[self.mino[2]][0]
            for j in range(r): dx, dy = dy, -dx
            temp[i] = [self.mino[0] + dx, self.mino[1] + dy]
        temp[3] = [self.mino[0], self.mino[1]]
        self.block = [i for i in self.mino]
        self.block[2] += 7
        overlap = 4
        while overlap != 0:
            overlap = 0
            self.block[1] -= 1
            if [self.block[0], self.block[1]] in temp: overlap += 1
            for i in range(3):
                dx = self.minos[self.block[2]][i + 1][0]
                dy = self.minos[self.block[2]][i + 1][1]
                r = self.block[3] % self.minos[self.block[2]][0]
                for j in range(r): dx, dy = dy, -dx
                if [self.block[0] + dx, self.block[1] + dy] in temp: overlap += 1
        if self.putMino(self.block):
            while self.putMino(self.block):
                self.deleteMino(self.block)
                self.block[1] -= 1
            self.block[1] += 1
            self.putMino(self.block)
        else:
            self.block = [i for i in self.mino]
            self.block[2] += 7

##  Player class에서 행동 명령을 받은 method.
##  0:  우회전
##  1:  좌회전
##  2:  아래 가기
##  3:  왼쪽 가기
##  4:  오른쪽 가기
##  5:  hold하기
##  6:  hard drop 하기
    def processInput(self, key):
        n = [i for i in self.mino]
        if key == 0: n[3] += 1
        if key == 1: n[3] -= 1
        elif key == 3: n[0] -= 1
        elif key == 4: n[0] += 1
        elif key == 5 and self.canHold:
            self.canHold = False
            if self.hold == None:
                self.hold = [5, 21, self.mino[2], 0]
                n = [5, 21, 0, 0]
                n[2] = self.selectMino()
            else: self.hold, n = [5, 21, self.mino[2], 0], [i for i in self.hold]
            for x in range(5):
                for y in range(5): self.board_hold[x][y] = 15
            self.board_hold[2][2] = self.hold[2]
            for i in range(3):
                dx = self.minos[self.hold[2]][i + 1][0]
                dy = self.minos[self.hold[2]][i + 1][1]
                self.board_hold[2 + dx][2 + dy] = self.hold[2]
            for j in range(5): self.board_hold[j].reverse()
        elif key == 6:
            n = [i for i in self.block]
            n[2] -= 7
        if n[0] != self.mino[0] or n[1] != self.mino[1] or n[2] != self.mino[2] or n[3] != self.mino[3]: 
            self.deleteMino(self.mino)
            if self.putMino(n): self.mino = [i for i in n]
            else: self.putMino(self.mino)

##  mino를 내려시키는 method. return값은 int(sound effect)
##  sound effect 종류
##  0: null
##  1: fall
##  2: line
##  3: allClear
##  4: damage
##  5: clear
    def minoDown(self):
        se = 0
        self.deleteMino(self.mino)
        self.mino[1] -= 1
        for i in range(len(self.attack)): self.attack[i] -= 1
        temp = []
        for i in self.attack:
            if i == 0: self.wall += 1
            elif i > 0: temp.append(i)
        self.attack = [i for i in temp]
        if not self.putMino(self.mino):
            self.mino[1] += 1
            self.putMino(self.mino)
            se = self.deleteLine()
            if self.wall > 0:
                self.makeWall()
                se = 4
            self.wall = 0
            self.canHold = True
            self.mino = [5, 21, 0, 0] # new mino
            self.mino[2] = self.selectMino()
            #gameOver
            if not self.putMino(self.mino): se = self.gameOver()
        return se

##  mino를 지울 수 있는지를 반단하고 지울 수있다면 지우고 공격을 계산하는 method. return값은 int(sound effect)
    def deleteLine(self):
        se = 1
        y = 1
        while y < 28:
            flag = True
            for x in range(1, 11):
                if self.board[x][y] == 0: flag = False
            if flag:
                for j in range(y, 28):
                    for i in range(1, 11): self.board[i][j] = self.board[i][j + 1]
                self.pawer += 1
                continue
            y += 1
        if self.pawer > 0: self.chain += 1
        else: self.chain = 0
        if self.pawer == 4:
            if self.btb:
                self.pawer += 1
##                print btb
            btb = True
##            print tetris
        elif self.pawer != 0:
            self.pawer -= 1
            btb = False
        flag = True
        for i in range(1, 11):
            if self.board[i][1] != 0:
                flag = False
                break
        if flag:
##            print allClear
            se = 3
            self.pawer = 10
        elif self.chain > 0: se = 2
        if self.chain > 1:
##            print chain
            if self.chain < 9: self.pawer += self.chain // 2
            elif self.chain == 10: self.pawer += 4
            else: self.pawer += 5
        self.pawer, temp = self.pawer - len(self.attack), self.pawer
        for i in range(len(self.attack)):
            if i < temp: self.attack[i] = -1
        if self.pawer < 0: self.pawer = 0
        self.pawer, self.wall = self.pawer - self.wall, self.wall - self.pawer
        if self.pawer < 0: self.pawer = 0
        if self.wall < 0: self.wall = 0
        return se

##  wall변수 에 있는 숫자 만큼 disturbing block를 random으로 틈새를 정해 만드는 method.
    def makeWall(self):
        n = random.randint(1, 10)
        for y in range(20, 0, -1):
            for x in range(1, 11):
                self.board[x][y + self.wall] = self.board[x][y]
                if y <= self.wall:
                    if x == n: self.board[x][y] = 0
                    else: self.board[x][y] = 15

##  Game class에서 상대방의 공격을 받아 attack list에 추가하는 method
    def setAttack(self, pawer):
        for i in range(pawer):
            if len(self.attack) >= 20: break
            self.attack.append(15)

##  Game class에서 mino list를 받는 method.
    def setMinoList(self, minoList):
        self.minoList = minoList

##  Game class에서 tick를 받아 time를 새는 method. time가 20으로 나눌 수 있을 때와 내리는 명령을 받았을 때 mino를 내려시킨다.
    def countTime(self, ret, pawer):
        se = 0
        self.setAttack(pawer)
        self.pawer = 0
        self.time += 1
        self.deleteMino(self.block)
        self.putMino(self.mino)
        if self.time % 20 == 0: se = self.minoDown()
        if ret:
            self.time = 0
            se = self.minoDown()
        return se

##  board에 있는 block를 disturbing block로 변환시키는 method. return값은 int(sound effect)
    def gameOver(self):
        for x in range(1, 11):
            for y in range(1, 21):
                if self.board[x][y] != 0: self.board[x][y] = 15
        return 5

##  board, board_hold, nexts, attack list를 return하는 method. return값은 list class
    def getLists(self):
        return [self.board, self.board_hold, self.nexts, self.attack]
