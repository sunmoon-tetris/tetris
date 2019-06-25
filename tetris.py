import random

class Tetris:
    def __init__(self):
        self.minos = [
            [1, [[0, 0], [0, 0], [0, 0]]],     ## null
            [2, [[0, -1], [0, 1], [0, 2]]],    ## I mino
            [4, [[0, -1], [0, 1], [1, 1]]],    ## J mino
            [4, [[0, -1], [0, 1], [-1, 1]]],   ## L mino
            [2, [[0, -1], [1, 0], [1, 1]]],    ## Z mino
            [2, [[0, -1], [-1, 0], [-1, 1]]],  ## S mino
            [1, [[0, 1], [1, 0], [1, 1]]],     ## O mino
            [4, [[0, -1], [1, 0], [-1, 0]]],   ## T mino
            [2, [[0, -1], [0, 1], [0, 2]]],    ## I mino for superDrop
            [4, [[0, -1], [0, 1], [1, 1]]],    ## J mino for superDrop
            [4, [[0, -1], [0, 1], [-1, 1]]],   ## L mino for superDrop
            [2, [[0, -1], [1, 0], [1, 1]]],    ## Z mino for superDrop
            [2, [[0, -1], [-1, 0], [-1, 1]]],  ## S mino for superDrop
            [1, [[0, 1], [1, 0], [1, 1]]],     ## O mino for superDrop
            [4, [[0, -1], [1, 0], [-1, 0]]]    ## T mino for superDrop
            ]
        self.board = [[0 for i in range(45)] for j in range(12)]
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if x == 0 or x == 11 or y == 0: self.board[x][y] = 1
        self.board_hold = [[15 for i in range(5)] for j in range(5)]
        self.nexts = [[[15 for i in range(5)] for j in range(5)] for k in range(5)]
        self.attack = []
        self.minoList = None
        self.cnt = 0
        self.pawer = 0
        self.wall = 0
        self.time = 0
        self.chain = 0
        self.canHold = True
        self.btb = False
        self.mino = [5, 21, 0, 0]
        self.block = [i for i in self.mino]
        self.hold = None

    def selectMino(self):
        for n in range(5):
            for x in range(5):
                for y in range(5): self.nexts[n][x][y] = 15
            nxt = self.cnt + n + 1
            self.nexts[n][2][2] = self.minoList[nxt // 7][nxt % 7]
            for i in range(3):
                dx = self.minos[self.minoList[nxt // 7][nxt % 7]][1][i][0]
                dy = self.minos[self.minoList[nxt // 7][nxt % 7]][1][i][1]
                self.nexts[n][2 + dx][2 + dy] = self.minoList[nxt // 7][nxt % 7]
        for j in range(5):
            for k in range(5): self.nexts[j][k].reverse()
        minoChoice = self.minoList[self.cnt // 7][self.cnt % 7]
        self.cnt += 1
        return minoChoice

    def putMino(self, mino, action = False):
        if self.board[mino[0]][mino[1]] != 0 and self.board[mino[0]][mino[1]] < 8\
           or self.board[mino[0]][mino[1]] == 15: return False
        if action: self.board[mino[0]][mino[1]] = mino[2]
        for i in range(3):
            dx = self.minos[mino[2]][1][i][0]
            dy = self.minos[mino[2]][1][i][1]
            r = mino[3] % self.minos[mino[2]][0]
            for j in range(r): dx, dy = dy, -dx
            if self.board[mino[0] + dx][mino[1] + dy] != 0 and self.board[mino[0] + dx][mino[1] + dy] < 8\
               or self.board[mino[0] + dx][mino[1] + dy] == 15: return False
            if action: self.board[mino[0] + dx][mino[1] + dy] = mino[2]
        if not action: self.putMino(mino, True)
        return True

    def deleteMino(self, mino):
        self.board[mino[0]][mino[1]] = 0
        for i in range(3):
            dx = self.minos[mino[2]][1][i][0]
            dy = self.minos[mino[2]][1][i][1]
            r = mino[3] % self.minos[mino[2]][0]
            for j in range(r): dx, dy = dy, -dx
            self.board[mino[0] + dx][mino[1] + dy] = 0

    def hardDrop(self):
        temp = [[] for i in range(4)]
        for i in range(3):
            dx = self.minos[self.mino[2]][1][i][0]
            dy = self.minos[self.mino[2]][1][i][1]
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
                dx = self.minos[self.block[2]][1][i][0]
                dy = self.minos[self.block[2]][1][i][1]
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

    def processInput(self, key):
        n = [i for i in self.mino]
        if key == 0: n[3] += 1
        elif key == 2: n[0] -= 1
        elif key == 3: n[0] += 1
        elif key == 4 and self.canHold:
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
                dx = self.minos[self.hold[2]][1][i][0]
                dy = self.minos[self.hold[2]][1][i][1]
                self.board_hold[2 + dx][2 + dy] = self.hold[2]
            for j in range(5): self.board_hold[j].reverse()
        elif key == 5:
            n = [i for i in self.block]
            n[2] -= 7
        if n[0] != self.mino[0] or n[1] != self.mino[1] or n[2] != self.mino[2] or n[3] != self.mino[3]: 
            self.deleteMino(self.mino)
            if self.putMino(n): self.mino = [i for i in n]
            else: self.putMino(self.mino)

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

    def makeWall(self):
        n = random.randint(1, 10)
        for y in range(20, 0, -1):
            for x in range(1, 11):
                self.board[x][y + self.wall] = self.board[x][y]
                if y <= self.wall:
                    if x == n: self.board[x][y] = 0
                    else: self.board[x][y] = 15

    def getLists(self):
        return [self.board, self.board_hold, self.nexts, self.attack]

    def setAttack(self, pawer):
        for i in range(pawer):
            if len(self.attack) >= 20: break
            self.attack.append(15)

    def setMinoList(self, minoList):
        self.minoList = minoList

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

    def gameOver(self):
        for x in range(1, 11):
            for y in range(1, 21):
                if self.board[x][y] != 0: self.board[x][y] = 15
        return 5
