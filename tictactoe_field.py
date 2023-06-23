from random import choice
from itertools import product


class GameField:
    FREE = 0
    HUMAN_X = 1
    DROID_O = 2
    DRAW = 3

    def __init__(self):
        self.field = [[self.FREE for _ in range(3)] for _ in range(3)]
        self.__win = self.FREE  # 1 - human, 2 - droid, 3 - draw
        self.__cells = list(product((0,1,2), repeat=2))
    
    @property
    def win(self):
        return self.__win
    
    def __getitem__(self, coords: tuple):
        r, c = coords
        return self.field[r][c] # (0 | 1 | 2)

    def __setitem__(self, coords: tuple, value: int):
        r, c = coords
        self.field[r][c] = value
        self.__cells.remove(coords)
        self.check_win(coords, value)

    def init(self):
        self.__init__()
        if choice((True, False)):
            self.droid()
    
    def check_win(self, coords: tuple, value: int):
        r, c = coords
        row = all((x == value for x in self.field[r]))  # check 1 row
        col = all((x[c] == value for x in self.field))  # check 1 column
        
        diag1 = diag2 = False
        if r == c:  # diagonal
            diag1 = all((self[i, i] == value for i in range(3)))
        if (r + c) == 2:  # antidiagonal
            diag2 = all((self[i, 2 - i] == value for i in range(3)))

        if any((row, col, diag1, diag2)):
            self.__win = value
            return
        
        if not self.__cells: # check draw
            self.__win = self.DRAW

    def human(self, coords: tuple):
        if self[coords] == self.FREE:
            self[coords] = self.HUMAN_X
            return True

    def droid(self):
        coords = self.droid_iq(self.DROID_O)
        if not coords:
            coords = self.droid_iq(self.HUMAN_X)
            if not coords:
                coords = choice(self.__cells)
        self[coords] = self.DROID_O

    def droid_iq(self, xo: int):
        diag1, diag2 = [], []
        for r in range(3):
            row, col = [], []
            for c in range(3):
                if r == c: # diagonal
                    diag1.append(self[r, c])
                if r + c == 2: # antidiagonal
                    diag2.append(self[r, c])
                row.append(self[r, c])
                col.append(self[c, r])
            if row.count(xo) == 2 and self.FREE in row:
                return r, row.index(self.FREE)
            
            if col.count(xo) == 2 and self.FREE in col:
                return col.index(self.FREE), r
            
        if diag1.count(xo) == 2 and self.FREE in diag1:
            return diag1.index(self.FREE), diag1.index(self.FREE)
        
        if diag2.count(xo) == 2 and self.FREE in diag2:
            return diag2.index(self.FREE), 2 - diag2.index(self.FREE)
        
        return False

    