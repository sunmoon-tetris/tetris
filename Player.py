##  Player class
##
##  tetris를 부는 프로그램.
##
##  varsion: 2019/07/05
##  author: Katsutoshi Eda

import numpy as np

class Player:
    def __init__(self):
        self.command = 0
        self.lists = None
        self.mino = None

##      Tetris class에서 board, board_hold, nexts, attack list를 받아 알고리즘을 통해 행동을 return한다.
##      block의 종류
##      1:  I mino
##      2:  J mino
##      3:  L mino
##      4:  Z mino
##      5:  S mino
##      6:  O mino
##      7:  T mino
##      8:  I mino of hard drop
##      9:  J mino of hard drop
##      10: L mino of hard drop
##      11: Z mino of hard drop
##      12: S mino of hard drop
##      13: O mino of hard drop
##      14: T mino of hard drop
##      15: disturbing block
##
##      board:  x: 12, y: 45로 구성. block이 없을 때 0. 벽은 1. block이 있을 때는 block의 종류.
##
##      board_hold: x: 5, y: 5로 구성. block이 없을 때 15. block이 있을 때는 board_hold[2][2]를 중심으로 저장. 숫자는 block의 종류.
##
##      nexts: 개수: 5, x: 5, y: 5로 구성. nexts[n][2][2]를 중심으로 저장. 숫자는 block의 종류.
##
##      attack: 상대방의공격을 저장 되어 있는 list. 15부터 시작하고 전전히 내린다. 0이 되면 disturbing block이 생긴다. 공격이 없을 때는 list의 length는 0.
##
##      return값은 int이고 각 숫자는 아래와 같다. 다른 숫자는 행동하지 않는다.
##      0:  우회전
##      1:  좌회전
##      2:  아래 가기
##      3:  왼쪽 가기
##      4:  오른쪽 가기
##      5:  hold하기
##      6:  hard drop 하기
    def getAction(self, lists, mino):
        self.lists = lists
        self.mino = mino
        self.command = np.random.randint(0, 7)
        return self.command
