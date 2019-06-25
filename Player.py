import random

class Player:
    def __init__(self):
        self.command = 0
        self.lists = None
        self.mino = None
    def answer(self, lists, mino):
        self.lists = lists
        self.mino = mino
        self.command = random.randint(0, 5)
        return self.command
