import customtkinter
from gamefield import GameField
from random import choice
import itertools
from time import sleep

DEBUG = False #FIXME
SIZE = 10

class App(customtkinter.CTk):
    def __init__(self, field_human, field_droid, size=10):
        super().__init__()

        self.title("SEABATTLE THE GAME")
        self.resizable(False, False)
        self.geometry("+70+70")

        self._fhuman = field_human
        self._fdroid = field_droid
        self._fhuman_get = field_human.get_field()
        self._fdroid_get = field_droid.get_field()
        
        self._size = size
        self.fire_cells = [(x, y) for x in range(self._size) for y in range(self._size)]
        self.fire_next = set()
        self.fire_memory = []

        # ============ create frames (2x1 +1) ============
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.frame_right = customtkinter.CTkFrame(master=self,
                                                  width=180,
                                                  corner_radius=0)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        if DEBUG:
            self.frame_bottom = customtkinter.CTkFrame(master=self,
                                                       width=180,
                                                       corner_radius=0)
            self.frame_bottom.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)

            self.testbutton = customtkinter.CTkButton(master=self.frame_bottom,
                                                      text='test',
                                                      command=self.test,
                                                      fg_color=None
                                                      ).grid(row=0, column=0)

        # ============ frame_left ============
        self.field_left = [[0] * self._size for _ in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
                self.field_left[i][j] = customtkinter.CTkButton(master=self.frame_left,
                                                                text='',
                                                                width=28,
                                                                border_color='white',
                                                                fg_color=self.cell_view_human(i, j))
                self.field_left[i][j].grid(row=i, column=j)

        # ============ frame_right ============
        self.field_right = [[0] * self._size for _ in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
                self.field_right[i][j] = customtkinter.CTkButton(master=self.frame_right,
                                                                 text='',
                                                                 width=28,
                                                                #  fg_color=self.cell_view_droid(i, j),
                                                                 command=lambda row=i, column=j: self.hit(row, column))
                self.field_right[i][j].grid(row=i, column=j)

    def cell_view_human(self, i, j):
        if self._fhuman_get[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self._fhuman_get[i][j] == 1:
            return 'grey'
        if self._fhuman_get[i][j] == 2:
            return 'red'
        if self._fhuman_get[i][j] == 3:
            return 'black'
        
    def cell_view_droid(self, i, j):
        if self._fdroid_get[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self._fdroid_get[i][j] == 1:
            return 'grey' if DEBUG else ["#3B8ED0", "#1F6AA5"]
        if self._fdroid_get[i][j] == 2:
            return 'red'
        if self._fdroid_get[i][j] == 3:
            return 'black'
        
    def flash(self, i, j):
        sleep(1)
        self.field_left[i][j].configure(border_width=4, text='+')
        self.update()
        sleep(1)
        self.field_left[i][j].configure(border_width=0, text='')

    def redraw(self):
        self._fhuman_get = field_human.get_field()
        self._fdroid_get = field_droid.get_field()
        for i in range(self._size):
            for j in range(self._size):
                self.field_left[i][j].configure(fg_color=self.cell_view_human(i, j))
                self.field_right[i][j].configure(fg_color=self.cell_view_droid(i, j))
        self.update()

    def hit(self, i, j):
        if self._fdroid.get_field()[i][j] == 1:
            self._fdroid.hit(i, j)
        self.redraw()
        self.droid()
        self._fdroid.move_ships()
        self._fhuman.move_ships()
        self.redraw()

    def droid(self):
        if self.fire_next:
            x, y = choice(tuple(self.fire_next))
            self.fire_next.remove((x, y))
        else:
            x, y = choice(self.fire_cells)
        print(x, y) #test
        self.flash(x, y)
        if self._fhuman.get_field()[x][y] == 1:
            self._fhuman.hit(x, y) # hit changes self._fhuman.get_field()[x][y]
            self.fire_memory.append((x, y))
            if self._fhuman.get_field()[x][y] == 2:
                # self.droid_iq_100(x, y)
                self.droid_iq_70()
            else: # if self._fhuman.get_field()[x][y] == 3 (ship dead)
                for x, y in self.fire_memory:
                    for a, b in itertools.product([-1,0,1], repeat=2):
                        try:
                            self.fire_cells.remove((x + a, y + b))
                        except:
                            continue
                self.fire_next = set()
                self.fire_memory = []

    def droid_iq_100(self, x, y):
        def add_next(x, y):
            if min(x, y) >= 0 and max(x, y) < self._size and (x, y) in self.fire_cells:
                self.fire_next.add((x, y))

        if len(self.fire_memory) < 2:
            for d in (-1, 1):
                _x = x + d
                _y = y + d
                add_next(_x, y)
                add_next(x, _y)
        else:
            mem = self.fire_memory
            maax = max(i[0] for i in mem), max(i[1] for i in mem)
            miin = min(i[0] for i in mem), min(i[1] for i in mem)
            if maax[0] - miin[0] == 0:
                maax = maax[0], maax[1] + 1
                miin = miin[0], miin[1] - 1
            else:
                maax = maax[0] + 1, maax[1]
                miin = miin[0] - 1, miin[1]
            self.fire_next = set()
            add_next(*maax)
            add_next(*miin)
        print(self.fire_next) #test

    def droid_iq_70(self):
        def add_next(x, y):
            if min(x, y) >= 0 and max(x, y) < self._size and (x, y) in self.fire_cells:
                self.fire_next.add((x, y))

        fhuman = self._fhuman.get_field()
        for i in range(self._size):
            for j in range(self._size):
                if fhuman[i][j] == 2:
                    for d in (-1, 1):
                        x, y = i + d, j
                        add_next(x, y)
                        x, y = i, j + d
                        add_next(x, y)
                    print(self.fire_next) #test
                
               
    def test(self):
        print(self.fire_next)
        print(self.fire_cells)
        # self._fhuman.show()
        # self._fdroid.show()
        # self._fhuman.move_ships()
        # self._fdroid.move_ships()
        # self.redraw()


if __name__ == "__main__":
    print('go')
    field_human = GameField(SIZE)
    field_human.init()
    field_droid = GameField(SIZE)
    field_droid.init()

    app = App(field_human, field_droid, size=SIZE)
    app.mainloop()

