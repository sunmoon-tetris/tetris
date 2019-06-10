import sys
import pygame
from pygame.locals import *
import cv2
import random

class game:
    def __init__(self):
        self.board = [[0 for i in range(28)] for i in range(12)]
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if x == 0 or x == 11 or y == 0:
                    self.board[x][y] = 1
        self.board_hold = [[15 for i in range(5)] for i in range(5)]
        self.nexts = [[[15 for i in range(5)] for i in range(5)] for i in range(5)]
        self.attack = [15 for i in range(20)]
        self.cnt = 0
        self.pawer = 0
        self.canHold = True
        self.btb = False
        

player1 = game(1)
player2 = game(2)
