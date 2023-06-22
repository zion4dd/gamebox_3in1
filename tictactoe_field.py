from random import randint

class Cell:
    def __init__(self, value=0):
        self.value = value
    
    def __bool__(self):
        return self.value == 0


class TicTacToe:
    FREE_CELL = 0      # свободная клетка
    HUMAN_X = 1        # крестик (игрок - человек)
    DROID_O = 2     # нолик (игрок - компьютер)

    def __init__(self):
        self.field = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.__win = 0  # 1 - human, 2 - droid, 3 - draw
    
    def check_win(self, r, c, value):
        row = all((x.value == value for x in self.field[r]))  # проверяем строку на выигрыш
        col = all((x[c].value == value for x in self.field))  # проверяем столбец на выигрыш
        diag1 = diag2 = False
        if r == c:  # если входит главная диагональ
            diag1 = all((self.field[i][i].value == value for i in range(3)))
        if (r + c) == 2:  # если входит побочная диагональ
            diag2 = all((self.field[i][-i+2].value == value for i in range(3)))

        if any((row, col, diag1, diag2)):
            if value == self.HUMAN_X:
                self.__win = 1
            else:
                self.__win = 2
            return
            
        # проверка на ничью
        if not any((x.value == self.FREE_CELL for row in self.field for x in row)):
            self.__win = 3

    def __getitem__(self, item):
        r, c = item
        return self.field[r][c].value # element or value

    def __setitem__(self, key, value):
        r, c = key
        self.field[r][c].value = value
        self.check_win(r, c, value)

    def init(self):
        self.__win = 0  # 1 - hum, 2 - comp, 3 - draw
        for row in self.field:
            for i in row:
                i.value = self.FREE_CELL
        if randint(0, 1):
            self.droid_go()
    
    def human_go(self, r, c):
        if self[r, c] == self.FREE_CELL:
            self[r, c] = self.HUMAN_X
            return True

    def droid_go(self):
        r, c = randint(0, 2), randint(0, 2)
        if self[r, c] == self.FREE_CELL:
            self[r, c] = self.DROID_O
        else:
            self.droid_go()
    
    @property
    def is_human_win(self):  # True, если победил человек
        return self.__win == 1

    @property
    def is_droid_win(self):  # True, если победил комп
        return self.__win == 2

    @property
    def is_draw(self):  # True, если ничья
        return self.__win == 3
    
    def __bool__(self):  # возвращает True, если игра не окончена
        return not any((self.is_human_win, self.is_droid_win, self.is_draw))

