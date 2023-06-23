from random import randint, choice
# x - row, y - column

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length
        self._tp = tp  # 1 || ; 2 ==
        self._x = x
        self._y = y
        self._is_move = True  # False after hit!
        self._cells = [1] * length  # 1 - ok, 2 - hit, 3 - dead

    @property
    def length(self):
        return self._length

    @property
    def tp(self):
        return self._tp
        
    """x2, y2 - coords of the ship-zone SE corner.
    ship-zone is the ship cells +1 cell right and down"""

    @property
    def x2(self):
        return self._x + self._length if self._tp == 1 else self._x + 1

    @property
    def y2(self):
        return self._y + self._length if self._tp == 2 else self._y + 1
    
    def __repr__(self) -> str:
        return str((self._x, self._y, self._tp))

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value

    def __iter__(self):
        """return ship cells coords and its values"""

        for i in range(self._length):
            if self._tp == 1:
                x = self._x + i
                y = self._y
            else:
                x = self._x
                y = self._y + i
            yield x, y, self[i]  # __getitem__

    def get_start_coords(self):
        return self._x, self._y

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def move(self, go: int):  # +1 | -1
        if self._is_move:
            if self._tp == 1:
                self.set_start_coords(self._x + go, self._y)
            else:
                self.set_start_coords(self._x, self._y + go)
            return True
        return False
        
    def is_collide(self, ship):  # -> True if 'ships collide' else False
        return not any((self._x > ship.x2, self.x2 < ship._x, self._y > ship.y2, self.y2 < ship._y))
                    # there is no ship collision if ONLY 1 condition is True
    
    def is_out_field(self, size):  # -> True if 'ship is out' else False
        return any((self._x < 0, self._y < 0, self.x2 > size, self.y2 > size))


class GameField:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self._life = 20

    def init(self):
        self.__init__()
        # create ships in order: from longest to shortest!
        ships = [Ship(4, tp=choice([1, 2])), Ship(3, tp=choice([1, 2])), 
                 Ship(3, tp=choice([1, 2])), Ship(2, tp=choice([1, 2])), 
                 Ship(2, tp=choice([1, 2])), Ship(2, tp=choice([1, 2])),
                 Ship(1, tp=choice([1, 2])), Ship(1, tp=choice([1, 2])),
                 Ship(1, tp=choice([1, 2])), Ship(1, tp=choice([1, 2]))]
        
        for ship in ships:  # put ships on field
            while True:
                if ship.tp == 1:
                    x = randint(0, self._size - ship.length)
                    y = randint(0, self._size - 1)
                else:
                    x = randint(0, self._size - 1)
                    y = randint(0, self._size - ship.length)

                ship.set_start_coords(x, y)
                if any(ship.is_collide(sh) for sh in self._ships):
                    continue

                self._ships.append(ship)
                break

    def get_field(self):
        field = [[0] * self._size for _ in range(self._size)]
        for ship in self._ships:
            for x, y, value in ship:
                field[x][y] = value
        return field

    def move_ships(self):
        def move_allowed():
            # print(ship, direction, end=' | ') #test
            if ship.is_out_field(self._size) or any(ship.is_collide(sh) for sh in self._ships if sh != ship):
                ship.set_start_coords(*x_y_backup)
                return False
            return True
        
        for ship in self._ships:
            direction = choice([-1, 1])
            x_y_backup = ship.get_start_coords()
            if ship.move(direction):
                if not move_allowed():
                    ship.move(-direction)
                    move_allowed() # to check and backup

    def hit(self, r, c):
        for ship in self._ships:
            x1, y1 = ship.get_start_coords()
            x2, y2 = ship.x2, ship.y2
            if x1 <= r < x2 and y1 <= c < y2:
                print(f'hit! row: {x1} <= {r} < {x2} | col: {y1} <= {c} < {y2}') #test
                self._life -= 1
                ship[max(r - x1, c - y1)] = 2
                ship._is_move = False
                if all(map(lambda x: x == 2, ship._cells)): # if dead
                    for r in range(ship.length):
                        ship[r] = 3
                break

    def show(self): #test
        print('    0 1 2 3 4 5 6 7 8 9')
        print('   --------------------')
        for i, row in enumerate(self.get_field()):
            print(i, '|', *row, sep=' ')

#test
if __name__ == "__main__":
    SIZE = 10

    field = GameField(SIZE)
    field.init()
    field.show()

    field.move_ships()
    print()
    field.show()

