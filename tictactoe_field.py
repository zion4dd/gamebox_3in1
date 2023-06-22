from random import choice
from itertools import product

class Cell:
    def __init__(self, value=0):
        self.value = value
    
    def __bool__(self):
        return self.value == 0


class GameField:
    FREE_CELL = 0
    HUMAN_X = 1
    DROID_O = 2

    def __init__(self):
        self.field = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.__win = 0  # 1 - human, 2 - droid, 3 - draw
        self.__cells = list(product((0,1,2), repeat=2))
    
    @property
    def win(self):
        return self.__win
    
    def __getitem__(self, item):
        r, c = item
        return self.field[r][c].value # return cell value (0|1|2)

    def __setitem__(self, key, value):
        r, c = key
        self.field[r][c].value = value
        self.check_win(r, c, value)

    def init(self):
        self.__init__()
        if choice((0, 1)):
            self.droid()
    
    def check_win(self, r, c, value):
        row = all((x.value == value for x in self.field[r]))  # check row
        col = all((x[c].value == value for x in self.field))  # check column
        diag1 = diag2 = False
        if r == c:  # diagonal
            diag1 = all((self.field[i][i].value == value for i in range(3)))
        if (r + c) == 2:  # antidiagonal
            diag2 = all((self.field[i][-i+2].value == value for i in range(3)))

        if any((row, col, diag1, diag2)):
            if value == self.HUMAN_X:
                self.__win = 1
            else:
                self.__win = 2
            return
        # draw check:
        if not any((x.value == self.FREE_CELL for row in self.field for x in row)):
            self.__win = 3

    def human(self, r, c):
        if self.field[r][c]:
            self[r, c] = self.HUMAN_X
            self.__cells.remove((r, c))
            return True

    def droid(self):
        coords = self.droid_iq(2)
        if not coords:
            coords = self.droid_iq(1)
            if not coords:
                coords = choice(self.__cells)
        self[*coords] = self.DROID_O
        self.__cells.remove(coords)

    def droid_iq(self, xo):
        d1, d2 = [], []
        for r in range(3):
            row, col = [], []
            for c in range(3):
                if r == c: # diagonal
                    d1.append(self[r, c])
                if r + c == 2: # antidiagonal
                    d2.append(self[r, c])
                row.append(self[r, c])
                col.append(self[c, r])
            if row.count(xo) == 2 and 0 in row:
                return r, row.index(0)
            
            if col.count(xo) == 2 and 0 in col:
                return col.index(0), r
            
        if d1.count(xo) == 2 and 0 in d1:
            return d1.index(0), d1.index(0)
        
        if d2.count(xo) == 2 and 0 in d2:
            return d2.index(0), 2 - d2.index(0)
        
        return False

    