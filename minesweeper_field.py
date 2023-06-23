from random import sample

class Cell:
    def __init__(self, around_mines=0, mine=False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.is_open = False

class GameField:
    def __init__(self, size, mines) -> None:
        self.__size = size
        self.__mines = mines
        self.__field = [Cell() for _ in range(self.__size) for __ in range(self.__size)]
                        # one-dimensional array
    def __getitem__(self, coords: tuple):
        r, c = coords
        return self.__field[self.__size * r + c]
    
    def init(self):
        self.__init__(self.__size, self.__mines)
        for cell in sample(self.__field, self.__mines):
            cell.mine = True

        for r in range(self.__size):
            for c in range(self.__size):
                cell = self.__field[self.__size * r + c]
                if cell.mine == True:
                    continue

                cell.around_mines = self.count(r, c)
    
    def count(self, r, c):
        result = 0
        for i in range(r-1, r+2):
            if 0 <= i < self.__size:
                for j in range(c-1, c+2):
                    if 0 <= j < self.__size:
                        if self.__field[self.__size * i + j].mine == True:
                            result += 1
        return result

