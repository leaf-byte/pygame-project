import pygame
import os
import sys
import random

pygame.init()
pygame.mixer.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "150, 150"

TETRAMINO = ("I0", "J0", "L0", "O", "S0", "T0", "Z0")
COLORS = {
    "I0": pygame.Color("cyan"), "I1": pygame.Color("cyan"), "J0": pygame.Color("blue"),
    "J1": pygame.Color("blue"), "J2": pygame.Color("blue"), "J3": pygame.Color("blue"),
    "L0": pygame.Color("orange"), "L1": pygame.Color("orange"), "L2": pygame.Color("orange"),
    "L3": pygame.Color("orange"), "O": pygame.Color("yellow"), "S0": pygame.Color("green"),
    "S1": pygame.Color("green"), "T0": pygame.Color("purple"), "T1": pygame.Color("purple"),
    "T2": pygame.Color("purple"), "T3": pygame.Color("purple"), "Z0": pygame.Color("red"),
    "Z1": pygame.Color("red")
}
RESULTS = {}
with open("data/records.txt", 'r', encoding="utf8") as fin:
    t = fin.read()
    if t:
        t = t.split("\n")[:-1]
        for m in t:
            k = m.split(' ')
            RESULTS[int(k[1])] = k[3]


class Figure(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.x = 4
        self.y = 0

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        if self.name == "I0":
            self.name = "I1"
            self.x -= 1
            self.y += 1
        elif self.name == "I1":
            self.name = "I0"
            self.x += 1
            self.y -= 1
        elif self.name == "J0":
            self.name = "J1"
            self.x -= 1
        elif self.name == "J1":
            self.name = "J2"
            self.x += 1
        elif self.name == "J2":
            self.name = "J3"
            self.x -= 1
            self.y += 1
        elif self.name == "J3":
            self.name = "J0"
            self.x += 1
            self.y -= 1
        elif self.name == "L0":
            self.name = "L1"
            self.x -= 1
            self.y += 1
        elif self.name == "L1":
            self.name = "L2"
            self.y -= 1
        elif self.name == "L2":
            self.name = "L3"
            self.x += 2
        elif self.name == "L3":
            self.name = "L0"
            self.x -= 1
        elif self.name == "O":
            pass
        elif self.name == "S0":
            self.name = "S1"
            self.y -= 1
        elif self.name == "S1":
            self.name = "S0"
            self.y += 1
        elif self.name == "T0":
            self.name = "T1"
            self.x += 2
        elif self.name == "T1":
            self.name = "T2"
            self.x -= 1
            self.y += 1
        elif self.name == "T2":
            self.name = "T3"
            self.x -= 1
            self.y -= 1
        elif self.name == "T3":
            self.name = "T0"
        elif self.name == "Z0":
            self.name = "Z1"
            self.x += 2
            self.y -= 1
        elif self.name == "Z1":
            self.name = "Z0"
            self.x -= 2
            self.y += 1


class Board:
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.cell_size = 28
        self.screen = screen
        self.board = [[0] * width for _ in range(height)]
        self.left = 400 - self.cell_size * width // 2
        self.top = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for x in range(self.left, self.left + self.cell_size * self.width, self.cell_size):
            for y in range(self.top, self.top + self.cell_size * self.height, self.cell_size):
                cell_x, cell_y = self.get_cell((x, y))
                sz = self.cell_size
                pygame.draw.rect(self.screen, (255, 255, 255), (x, y, sz, sz))
                if self.board[cell_y][cell_x] == 0:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x + 1, y + 1, sz - 2, sz - 2))
                else:
                    pygame.draw.rect(self.screen, self.board[cell_y][cell_x],
                                     (x + 1, y + 1, sz - 2, sz - 2))

    def get_cell(self, pos):
        x, y = pos
        if self.left <= x <= self.left + self.cell_size * self.width:
            if self.top <= y <= self.top + self.cell_size * self.height:
                cell_x = (x - self.left) // self.cell_size
                cell_y = (y - self.top) // self.cell_size
                return cell_x, cell_y

    def can_create(self):
        return (all(map(lambda x: x == 0, self.board[3])) and
                all(map(lambda x: x == 0, self.board[2])) and
                all(map(lambda x: x == 0, self.board[1])) and
                all(map(lambda x: x == 0, self.board[0])))

    def create(self, figure):
        if figure.name == "I0":
            for i in range(4):
                self.board[i][figure.x] = COLORS[figure.name]
        elif figure.name == "I1":
            for i in range(figure.x, figure.x + 4):
                self.board[figure.y][i] = COLORS[figure.name]
        elif figure.name == "J0":
            for i in range(3):
                self.board[i][figure.x] = COLORS[figure.name]
            self.board[2][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "J1":
            self.board[0][figure.x] = COLORS[figure.name]
            for i in range(figure.x, figure.x + 3):
                self.board[1][i] = COLORS[figure.name]
        elif figure.name == "J2":
            for i in range(3):
                self.board[i][figure.x] = COLORS[figure.name]
            self.board[0][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J3":
            self.board[1][figure.x + 2] = COLORS[figure.name]
            for i in range(figure.x, figure.x + 3):
                self.board[0][i] = COLORS[figure.name]
        elif figure.name == "L0":
            for i in range(3):
                self.board[i][figure.x] = COLORS[figure.name]
            self.board[2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L1":
            for i in range(figure.x, figure.x + 3):
                self.board[0][i] = COLORS[figure.name]
            self.board[1][figure.x] = COLORS[figure.name]
        elif figure.name == "L2":
            for i in range(3):
                self.board[i][figure.x + 1] = COLORS[figure.name]
            self.board[0][figure.x] = COLORS[figure.name]
        elif figure.name == "L3":
            for i in range(figure.x - 2, figure.x + 1):
                self.board[1][i] = COLORS[figure.name]
            self.board[0][figure.x] = COLORS[figure.name]
        elif figure.name == "O":
            for i in range(2):
                self.board[i][figure.x] = COLORS[figure.name]
                self.board[i][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "S0":
            self.board[0][figure.x + 1] = COLORS[figure.name]
            self.board[1][figure.x - 1] = COLORS[figure.name]
            for i in range(2):
                self.board[i][figure.x] = COLORS[figure.name]
        elif figure.name == "S1":
            for i in range(2):
                self.board[i][figure.x] = COLORS[figure.name]
            for i in range(1, 3):
                self.board[i][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "T0":
            self.board[0][figure.x] = COLORS[figure.name]
            self.board[0][figure.x + 2] = COLORS[figure.name]
            for i in range(2):
                self.board[i][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "T1":
            for i in range(3):
                self.board[i][figure.x] = COLORS[figure.name]
            self.board[1][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "T2":
            for i in range(figure.x - 1, figure.x + 2):
                self.board[1][i] = COLORS[figure.name]
            self.board[0][figure.x] = COLORS[figure.name]
        elif figure.name == "T3":
            for i in range(3):
                self.board[i][figure.x] = COLORS[figure.name]
            self.board[1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "Z0":
            self.board[0][figure.x] = COLORS[figure.name]
            self.board[1][figure.x + 2] = COLORS[figure.name]
            for i in range(2):
                self.board[i][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "Z1":
            for i in range(1, 3):
                self.board[i][figure.x - 1] = COLORS[figure.name]
            for i in range(2):
                self.board[i][figure.x] = COLORS[figure.name]

    def can_move_down(self, figure):
        if figure.name == "I0":
            return figure.y < 16 and self.board[figure.y + 4][figure.x] == 0
        elif figure.name == "I1":
            if figure.y == 19:
                return False
            if self.board[figure.y + 1][figure.x] != 0:
                return False
            if self.board[figure.y + 1][figure.x + 1] != 0:
                return False
            if self.board[figure.y + 1][figure.x + 2] != 0:
                return False
            if self.board[figure.y + 1][figure.x + 3] != 0:
                return False
            return True
        elif figure.name == "J0":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 3][figure.x] == 0 and
                    self.board[figure.y + 3][figure.x - 1] == 0)
        elif figure.name == "J1":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "J2":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 3][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "J3":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "L0":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 3][figure.x] == 0 and
                    self.board[figure.y + 3][figure.x + 1] == 0)
        elif figure.name == "L1":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "L2":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 3][figure.x + 1] == 0)
        elif figure.name == "L3":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x - 2] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)
        elif figure.name == "O":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "S0":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "S1":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 3][figure.x + 1] == 0)
        elif figure.name == "T0":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "T1":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 3][figure.x] == 0)
        elif figure.name == "T2":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "T3":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 3][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "Z0":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "Z1":
            if figure.y > 16:
                return False
            return (self.board[figure.y + 3][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)

    def move_down(self, figure):
        if figure.name == "I0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 4][figure.x] = COLORS[figure.name]
        elif figure.name == "I1":
            for i in range(figure.x, figure.x + 4):
                self.board[figure.y][i] = 0
                self.board[figure.y + 1][i] = COLORS[figure.name]
        elif figure.name == "J0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x - 1] = 0
            self.board[figure.y + 3][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x] = COLORS[figure.name]
        elif figure.name == "J1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1: figure.x + 3] = [0, 0]
            self.board[figure.y + 2][figure.x: figure.x + 3] = [
                COLORS[figure.name], COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "J2":
            self.board[figure.y][figure.x: figure.x + 2] = [0, 0]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x] = COLORS[figure.name]
        elif figure.name == "J3":
            self.board[figure.y][figure.x: figure.x + 3] = [0, 0, 0]
            self.board[figure.y + 1][figure.x: figure.x + 2] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
            self.board[figure.y + 2][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "L0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y + 3][figure.x: figure.x + 2] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "L1":
            self.board[figure.y][figure.x: figure.x + 3] = [0, 0, 0]
            self.board[figure.y + 1][figure.x + 1: figure.x + 3] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
        elif figure.name == "L2":
            self.board[figure.y][figure.x: figure.x + 2] = [0, 0]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 2: figure.x] = [0, 0]
            self.board[figure.y + 2][figure.x - 2: figure.x + 1] = [
                COLORS[figure.name], COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "O":
            self.board[figure.y][figure.x: figure.x + 2] = [0, 0]
            self.board[figure.y + 2][figure.x: figure.x + 2] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "S0":
            self.board[figure.y][figure.x: figure.x + 2] = [0, 0]
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1: figure.x + 1] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "S1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "T0":
            self.board[figure.y][figure.x: figure.x + 3] = [0, 0, 0]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "T1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x] = COLORS[figure.name]
        elif figure.name == "T2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x - 1: figure.x + 2] = [
                COLORS[figure.name], COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "T3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x] = COLORS[figure.name]
        elif figure.name == "Z0":
            self.board[figure.y][figure.x: figure.x + 2] = [0, 0]
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1: figure.x + 3] = [
                COLORS[figure.name], COLORS[figure.name]
            ]
        elif figure.name == "Z1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
            self.board[figure.y + 3][figure.x - 1] = COLORS[figure.name]

    def can_move_left(self, figure):
        if figure.name == "I0":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 3][figure.x - 1] == 0)
        elif figure.name == "I1":
            if figure.x == 0:
                return False
            return self.board[figure.y][figure.x - 1] == 0
        elif figure.name == "J0":
            if figure.x == 1:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 2] == 0)
        elif figure.name == "J1":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0)
        elif figure.name == "J2":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0)
        elif figure.name == "J3":
            if figure.x == 0:
                return True
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "L0":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0)
        elif figure.name == "L1":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0)
        elif figure.name == "L2":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x] == 0)
        elif figure.name == "L3":
            if figure.x == 2:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 3] == 0)
        elif figure.name == "O":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0)
        elif figure.name == "S0":
            if figure.x == 1:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 2] == 0)
        elif figure.name == "S1":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)
        elif figure.name == "T0":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x] == 0)
        elif figure.name == "T1":
            if figure.x == 1:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 2] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0)
        elif figure.name == "T2":
            if figure.x == 1:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 2] == 0)
        elif figure.name == "T3":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0)
        elif figure.name == "Z0":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x] == 0)
        elif figure.name == "Z1":
            if figure.x == 1:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 2] == 0 and
                    self.board[figure.y + 2][figure.x - 2] == 0)

    def move_left(self, figure):
        if figure.name == "I0":
            for i in range(figure.y, figure.y + 4):
                self.board[i][figure.x] = 0
                self.board[i][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "I1":
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y][figure.x + 3] = 0
        elif figure.name == "J0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 2] = COLORS[figure.name]
        elif figure.name == "J1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "J2":
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "J3":
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "L0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "L1":
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "L2":
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
        elif figure.name == "L3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 3] = COLORS[figure.name]
        elif figure.name == "O":
            for i in range(figure.y, figure.y + 2):
                self.board[i][figure.x - 1] = COLORS[figure.name]
                self.board[i][figure.x + 1] = 0
        elif figure.name == "S0":
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 2] = COLORS[figure.name]
        elif figure.name == "S1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
        elif figure.name == "T0":
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
        elif figure.name == "T1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 2] = COLORS[figure.name]
        elif figure.name == "T2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 2] = COLORS[figure.name]
        elif figure.name == "T3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "Z0":
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
        elif figure.name == "Z1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x - 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 2] = COLORS[figure.name]

    def can_move_right(self, figure):
        if figure.name == "I0":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0 and
                    self.board[figure.y + 3][figure.x + 1] == 0)
        elif figure.name == "I1":
            return figure.x != 6 and self.board[figure.y][figure.x + 4] == 0
        elif figure.name == "J0":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "J1":
            if figure.x == 7:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 3] == 0)
        elif figure.name == "J2":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "J3":
            if figure.x == 7:
                return False
            return (self.board[figure.y][figure.x + 3] == 0 and
                    self.board[figure.y + 1][figure.x + 3] == 0)
        elif figure.name == "L0":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "L1":
            if figure.x == 7:
                return False
            return (self.board[figure.y][figure.x + 3] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "L2":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "L3":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "O":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "S0":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "S1":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "T0":
            if figure.x == 7:
                return False
            return (self.board[figure.y][figure.x + 3] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "T1":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "T2":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "T3":
            if figure.x == 8:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "Z0":
            if figure.x == 7:
                return False
            return (self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 3] == 0)
        elif figure.name == "Z1":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)

    def move_right(self, figure):
        if figure.name == "I0":
            for i in range(figure.y, figure.y + 4):
                self.board[i][figure.x] = 0
                self.board[i][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "I1":
            self.board[figure.y][figure.x + 4] = COLORS[figure.name]
            self.board[figure.y][figure.x] = 0
        elif figure.name == "J0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x - 1] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 3] = COLORS[figure.name]
        elif figure.name == "J2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x + 3] = COLORS[figure.name]
            self.board[figure.y][figure.x + 3] = COLORS[figure.name]
        elif figure.name == "L0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "L1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x + 3] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "L3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 2] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "O":
            for i in range(figure.y, figure.y + 2):
                self.board[i][figure.x + 2] = COLORS[figure.name]
                self.board[i][figure.x] = 0
        elif figure.name == "S0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "S1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "T0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y][figure.x + 3] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "T1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "T2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "T3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "Z0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 3] = COLORS[figure.name]
        elif figure.name == "Z1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y + 2][figure.x - 1] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]

    def can_rotate(self, figure):
        if figure.name == "I0":
            if figure.x == 0:
                return False
            if figure.x > 7:
                return False
            return (self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "I1":
            if figure.y == 0:
                return False
            if figure.y > 17:
                return False
            return (self.board[figure.y - 1][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "J0":
            if figure.x == 9:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "J1":
            if figure.y > 17:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "J2":
            if figure.x == 0:
                return False
            return (self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0 and
                    self.board[figure.y + 2][figure.x + 1] == 0)
        elif figure.name == "J3":
            if figure.y == 0:
                return False
            return (self.board[figure.y - 1][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "L0":
            if figure.x == 0:
                return False
            return (self.board[figure.y + 1][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "L1":
            if figure.y == 1:
                return False
            return (self.board[figure.y - 1][figure.x] == 0 and
                    self.board[figure.y - 1][figure.x + 1] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "L2":
            if figure.x == 8:
                return False
            return (self.board[figure.y + 1][figure.x] == 0 and
                    self.board[figure.y][figure.x + 2] == 0 and
                    self.board[figure.y + 1][figure.x + 2] == 0)
        elif figure.name == "L3":
            if figure.x == 0:
                return False
            return (self.board[figure.y][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)
        elif figure.name == "O":
            return False
        elif figure.name == "S0":
            if figure.y == 0:
                return False
            return (self.board[figure.y - 1][figure.x] == 0 and
                    self.board[figure.y + 1][figure.x + 1] == 0)
        elif figure.name == "S1":
            if figure.x == 0:
                return False
            return (self.board[figure.y + 2][figure.x] == 0 and
                    self.board[figure.y + 2][figure.x - 1] == 0)
        elif figure.name == "T0":
            if figure.y > 17:
                return False
            return (self.board[figure.y + 1][figure.x + 2] == 0 and
                    self.board[figure.y + 2][figure.x + 2] == 0)
        elif figure.name == "T1":
            if figure.x < 2:
                return False
            return (self.board[figure.y + 2][figure.x - 1] == 0 and
                    self.board[figure.y + 2][figure.x - 2] == 0)
        elif figure.name == "T2":
            if figure.y == 0:
                return False
            return (self.board[figure.y - 1][figure.x - 1] == 0 and
                    self.board[figure.y][figure.x - 1] == 0)
        elif figure.name == "T3":
            if figure.x > 7:
                return False
            return (self.board[figure.y][figure.x + 1] == 0 and
                    self.board[figure.y][figure.x + 2] == 0)
        elif figure.name == "Z0":
            if figure.y == 0:
                return False
            return (self.board[figure.y - 1][figure.x + 2] == 0 and
                    self.board[figure.y][figure.x + 2] == 0)
        elif figure.name == "Z1":
            if figure.x < 2:
                return False
            return (self.board[figure.y + 1][figure.x - 2] == 0 and
                    self.board[figure.y + 2][figure.x] == 0)

    def rotate(self, figure):
        if figure.name == "I0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y + 3][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "I1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y][figure.x + 3] = 0
            self.board[figure.y - 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y + 2][figure.x - 1] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "J3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y - 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y][figure.x + 2] = 0
            self.board[figure.y - 1][figure.x] = COLORS[figure.name]
            self.board[figure.y - 1][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "L2":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x] = COLORS[figure.name]
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "L3":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 1][figure.x - 2] = 0
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
        elif figure.name == "S0":
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 1][figure.x - 1] = 0
            self.board[figure.y - 1][figure.x] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x + 1] = COLORS[figure.name]
        elif figure.name == "S1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 2][figure.x + 1] = 0
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "T0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y][figure.x + 1] = 0
            self.board[figure.y + 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "T1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y + 2][figure.x - 2] = COLORS[figure.name]
        elif figure.name == "T2":
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 1][figure.x + 1] = 0
            self.board[figure.y - 1][figure.x - 1] = COLORS[figure.name]
            self.board[figure.y][figure.x - 1] = COLORS[figure.name]
        elif figure.name == "T3":
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = 0
            self.board[figure.y][figure.x + 1] = COLORS[figure.name]
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "Z0":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x + 2] = 0
            self.board[figure.y - 1][figure.x + 2] = COLORS[figure.name]
            self.board[figure.y][figure.x + 2] = COLORS[figure.name]
        elif figure.name == "Z1":
            self.board[figure.y][figure.x] = 0
            self.board[figure.y + 1][figure.x] = 0
            self.board[figure.y + 2][figure.x] = COLORS[figure.name]
            self.board[figure.y + 1][figure.x - 2] = COLORS[figure.name]

    def delete_lines(self, score):
        for i in range(19, -1, -1):
            if all(map(lambda x: x != 0, self.board[i])):
                for j in range(i, 0, -1):
                    self.board[j][:] = self.board[j - 1][:]
                self.board[0][:] = [0] * 10
                score += 100
        return score


def menu():
    menu_w, menu_h = 600, 500
    menu_size = menu_w, menu_h
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(640 - menu_w // 2) + ", " + str(350 - menu_h // 2)
    menu_screen = pygame.display.set_mode(menu_size)
    running = True
    on_play = on_records = False
    menu_color = (0, 0, 0)
    font_color = (70, 230, 120)
    fullname = "data/tetris_wp.png"
    image = pygame.transform.scale(pygame.image.load(fullname).convert(), (menu_w + 250, menu_h))
    menu_screen.blit(image, (-150, -50))

    font = pygame.font.Font("data/font.ttf", 150)
    text = font.render("Tetris", 1, (255, 204, 0))
    text_x = menu_w // 2 - text.get_width() // 2
    text_y = 20
    menu_screen.blit(text, (text_x, text_y))

    font = pygame.font.Font("data/font.ttf", 70)
    text = font.render("Play", 1, font_color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = menu_w // 2 - text_w // 2
    text_y = 270
    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                     (text_x + text_w, text_y + text_h - 5), 5)
    play_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h)
    menu_screen.blit(text, (text_x, text_y))

    text = font.render("Records", 1, font_color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = menu_w // 2 - text_w // 2
    text_y = 350
    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                     (text_x + text_w, text_y + text_h - 5), 5)
    records_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h)
    menu_screen.blit(text, (text_x, text_y))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 285 and event.mod == 256:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(menu_screen, menu_color, play_rect)
                if play_rect.collidepoint(*event.pos):
                    font = pygame.font.Font("data/font.ttf", 80)
                    text = font.render("Play", 1, font_color)
                    text_w = text.get_width()
                    text_h = text.get_height()
                    text_x = menu_w // 2 - text_w // 2
                    text_y = 270
                    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                                     (text_x + text_w, text_y + text_h - 5), 5)
                    play_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h)
                    menu_screen.blit(text, (text_x, text_y))
                    on_records = False
                    on_play = not on_records
                else:
                    font = pygame.font.Font("data/font.ttf", 70)
                    text = font.render("Play", 1, font_color)
                    text_w = text.get_width()
                    text_h = text.get_height()
                    text_x = menu_w // 2 - text_w // 2
                    text_y = 270
                    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                                     (text_x + text_w, text_y + text_h - 5), 5)
                    play_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h + 10)
                    menu_screen.blit(text, (text_x, text_y))
                    on_play = False
                pygame.draw.rect(menu_screen, menu_color, records_rect)
                if records_rect.collidepoint(*event.pos):
                    font = pygame.font.Font("data/font.ttf", 80)
                    text = font.render("Records", 1, font_color)
                    text_w = text.get_width()
                    text_h = text.get_height()
                    text_x = menu_w // 2 - text_w // 2
                    text_y = 350
                    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                                     (text_x + text_w, text_y + text_h - 5), 5)
                    records_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h)
                    menu_screen.blit(text, (text_x, text_y))
                    on_records = True
                    on_play = not on_records
                else:
                    font = pygame.font.Font("data/font.ttf", 70)
                    text = font.render("Records", 1, font_color)
                    text_w = text.get_width()
                    text_h = text.get_height()
                    text_x = menu_w // 2 - text_w // 2
                    text_y = 350
                    pygame.draw.line(menu_screen, font_color, (text_x, text_y + text_h - 5),
                                     (text_x + text_w, text_y + text_h - 5), 5)
                    records_rect = pygame.Rect(text_x, text_y, text_w + 5, text_h)
                    menu_screen.blit(text, (text_x, text_y))
                    on_records = False
            if event.type == pygame.MOUSEBUTTONUP:
                if on_play:
                    running = False
                    choose_difficulty()
                elif on_records:
                    running = False
                    records()
        pygame.display.flip()


def choose_difficulty():
    choose_w, choose_h = 500, 300
    choose_size = choose_w, choose_h
    font_color = (0, 128, 192)
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(640 - choose_w // 2) + ", " + str(350 - choose_h // 2)
    choose_screen = pygame.display.set_mode(choose_size)
    choose_screen_color = (0, 0, 0)
    choose_screen.fill(choose_screen_color)
    choose = ""
    running = True

    font = pygame.font.Font("data/font.ttf", 50)
    text = font.render("Choose a difficulty", 1, font_color)
    text_w = text.get_width()
    text_x = choose_w // 2 - text_w // 2
    text_y = 50
    choose_screen.blit(text, (text_x, text_y))

    font = pygame.font.Font("data/font.ttf", 70)
    text = font.render("Easy", 1, font_color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = 40
    text_y = 150
    easy_rect = pygame.Rect(text_x, text_y, text_w, text_h)
    choose_screen.blit(text, (text_x, text_y))

    font = pygame.font.Font("data/font.ttf", 70)
    text = font.render("Middle", 1, font_color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = choose_w // 2 - text_w // 2
    text_y = 150
    middle_rect = pygame.Rect(text_x, text_y, text_w, text_h)
    choose_screen.blit(text, (text_x, text_y))

    font = pygame.font.Font("data/font.ttf", 70)
    text = font.render("Hard", 1, font_color)
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = 360
    text_y = 150
    hard_rect = pygame.Rect(text_x, text_y, text_w, text_h)
    choose_screen.blit(text, (text_x, text_y))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu()
            if event.type == pygame.MOUSEMOTION:
                if easy_rect.collidepoint(*event.pos):
                    choose = "easy"
                elif middle_rect.collidepoint(*event.pos):
                    choose = "middle"
                elif hard_rect.collidepoint(*event.pos):
                    choose = "hard"
                else:
                    choose = ""
            if event.type == pygame.MOUSEBUTTONUP:
                if choose:
                    play(choose)
            if event.type == pygame.KEYDOWN:
                if event.key == 285 and event.mod == 256:
                    running = False
                    menu()
        pygame.draw.rect(choose_screen, choose_screen_color, easy_rect)
        if choose == "easy":
            font = pygame.font.Font("data/font.ttf", 80)
            text = font.render("Easy", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = 30
            text_y = 145
            easy_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        else:
            font = pygame.font.Font("data/font.ttf", 70)
            text = font.render("Easy", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = 40
            text_y = 150
            easy_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        pygame.draw.rect(choose_screen, choose_screen_color, middle_rect)
        if choose == "middle":
            font = pygame.font.Font("data/font.ttf", 80)
            text = font.render("Middle", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = choose_w // 2 - text_w // 2
            text_y = 145
            middle_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        else:
            font = pygame.font.Font("data/font.ttf", 70)
            text = font.render("Middle", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = choose_w // 2 - text_w // 2
            text_y = 150
            middle_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        pygame.draw.rect(choose_screen, choose_screen_color, hard_rect)
        if choose == "hard":
            font = pygame.font.Font("data/font.ttf", 80)
            text = font.render("Hard", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = 350
            text_y = 145
            hard_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        else:
            font = pygame.font.Font("data/font.ttf", 70)
            text = font.render("Hard", 1, font_color)
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = 360
            text_y = 150
            hard_rect = pygame.Rect(text_x, text_y, text_w, text_h)
            choose_screen.blit(text, (text_x, text_y))
        pygame.display.flip()


def play(difficulty):
    if difficulty == "easy":
        fps = 4
    elif difficulty == "middle":
        fps = 5
    else:
        fps = 6

    pygame.mixer.music.load("data/tetris_theme.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(1.0)
    play_w, play_h = 800, 600
    play_size = play_w, play_h
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(640 - play_w // 2) + ", " + str(350 - play_h // 2)
    play_screen = pygame.display.set_mode(play_size)
    play_screen_color = (0, 0, 0)
    play_screen.fill(play_screen_color)
    clock = pygame.time.Clock()
    running = True
    paused = False
    muted = False

    pause_rect = pygame.Rect(720, 20, 50, 50)
    pygame.draw.rect(play_screen, (255, 255, 255), pause_rect)
    pygame.draw.rect(play_screen, (0, 0, 0), (730, 30, 10, 30))
    pygame.draw.rect(play_screen, (0, 0, 0), (750, 30, 10, 30))

    sound_rect = pygame.Rect(660, 20, 50, 50)
    pygame.draw.rect(play_screen, (255, 255, 255), sound_rect)
    fullname = "data/sound_on.png"
    sound_img = pygame.transform.scale(pygame.image.load(fullname).convert_alpha(), (40, 40))
    play_screen.blit(sound_img, (665, 25))

    board = Board(play_screen, 10, 20)
    score = 0
    queue = [random.choice(TETRAMINO) for _ in range(1000)]
    current = Figure(queue.pop(0))
    board.create(current)

    font = pygame.font.Font("data/font.ttf", 100)
    text = font.render("Score", 1, (0, 255, 255))
    text_x = 580
    text_y = 200
    play_screen.blit(text, (text_x, text_y))

    text = font.render(str(score), 1, (0, 255, 255))
    text_x = 580
    text_y = 300
    play_screen.blit(text, (text_x, text_y))

    while running:
        if paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
                    menu()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_rect.collidepoint(*event.pos):
                        if paused:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                        paused = not paused
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if paused:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    paused = not paused
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(*event.pos):
                    if paused:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    paused = not paused
                if sound_rect.collidepoint(*event.pos):
                    if muted:
                        pygame.mixer.music.unpause()
                        fullname = "data/sound_on.png"
                        sound_img = pygame.transform.scale(
                            pygame.image.load(fullname).convert_alpha(), (40, 40))
                        play_screen.blit(sound_img, (665, 25))
                    else:
                        pygame.mixer.music.pause()
                        fullname = "data/sound_off.png"
                        sound_img = pygame.transform.scale(
                            pygame.image.load(fullname).convert_alpha(), (40, 40))
                        play_screen.blit(sound_img, (665, 25))
                    muted = not muted
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if paused:
                        pygame.mixer.music.unpause()
                        fullname = "data/sound_on.png"
                        sound_img = pygame.transform.scale(
                            pygame.image.load(fullname).convert_alpha(), (40, 40))
                        play_screen.blit(sound_img, (665, 25))
                    else:
                        pygame.mixer.music.pause()
                        fullname = "data/sound_off.png"
                        sound_img = pygame.transform.scale(
                            pygame.image.load(fullname).convert_alpha(), (40, 40))
                        play_screen.blit(sound_img, (665, 25))
                    paused = not paused
                if event.key == pygame.K_m:
                    if muted:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    muted = not muted
                if event.key == 285 and event.mod == 256:
                    running = False
                    pygame.mixer.music.stop()
                    menu()
                if event.key == pygame.K_LEFT:
                    if board.can_move_left(current):
                        board.move_left(current)
                        current.move_left()
                if event.key == pygame.K_RIGHT:
                    if board.can_move_right(current):
                        board.move_right(current)
                        current.move_right()
                if event.key == pygame.K_UP:
                    if board.can_rotate(current):
                        board.rotate(current)
                        current.rotate()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("data/tetris_theme.mp3")
            pygame.mixer.music.play()
        if board.can_move_down(current):
            board.move_down(current)
            current.move_down()
        else:
            score = board.delete_lines(score)
            current = Figure(queue.pop(0))
            if board.can_create():
                board.create(current)
            else:
                pygame.mixer.music.stop()
                running = False
                pygame.quit()
                game_over(score)
        pygame.draw.rect(play_screen, (0, 0, 0),
                         (text_x, text_y, text.get_width(), text.get_height()))
        text = font.render(str(score), 1, (0, 255, 255))
        text_x = 580
        text_y = 300
        play_screen.blit(text, (text_x, text_y))
        clock.tick(fps)
        board.render()
        pygame.display.flip()


def game_over(score):
    pygame.init()
    gameover_w, gameover_h = 400, 400
    gameover_size = gameover_w, gameover_h
    os.environ['SDL_VIDEO_WINDOW_POS'] = \
        str(640 - gameover_w // 2) + ", " + str(350 - gameover_h // 2)
    gameover_screen = pygame.display.set_mode(gameover_size)
    font = pygame.font.Font("data/font.ttf", 100)
    text = font.render("Score", 1, (0, 255, 255))
    text_x = 200 - text.get_width() // 2
    text_y = 50
    gameover_screen.blit(text, (text_x, text_y))

    text = font.render(str(score), 1, (0, 255, 255))
    text_x = 200 - text.get_width() // 2
    text_y = 200
    gameover_screen.blit(text, (text_x, text_y))
    running = True
    name = input("What's your name?  ")
    recs = [score]
    RESULTS[score] = name

    with open("data/records.txt", 'r', encoding="utf8") as finp:
        t1 = finp.read()
        if t1:
            for i in t1.split("\n"):
                if i == '':
                    continue
                j = i.split(' ')
                recs.append(int(j[1]))
                RESULTS[int(j[1])] = j[3]
            recs.sort(reverse=True)
            if len(recs) > 10:
                RESULTS.pop(recs[10])
                recs = recs[:10]

    with open("data/records.txt", 'w', encoding="utf8") as fout:
        for i in range(len(recs)):
            fout.write(f"{i + 1}. {recs[i]} - {RESULTS[recs[i]]}\n")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu()
        pygame.display.flip()


def records():
    records_w, records_h = 600, 600
    records_size = records_w, records_h
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(640 - records_w // 2) + ", " + str(350 - records_h // 2)
    records_screen = pygame.display.set_mode(records_size)
    records_screen_color = (255, 255, 255)
    records_screen.fill(records_screen_color)
    fullname = "data/cup.png"
    image = pygame.transform.scale(pygame.image.load(fullname).convert_alpha(), (200, 240))
    records_screen.blit(image, (370, 330))
    running = True

    with open("data/records.txt", 'r') as f:
        res = f.read().split("\n")
        font = pygame.font.Font("data/font.ttf", 80)
        for i in range(len(res)):
            if not res[i]:
                continue
            text = font.render(res[i], 1, (90, 255, 90))
            text_x = 40
            text_y = 50 * (i + 1)
            records_screen.blit(text, (text_x, text_y))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu()
            if event.type == pygame.KEYDOWN:
                if event.key == 285 and event.mod == 256:
                    running = False
                    menu()
        pygame.display.flip()


menu()
