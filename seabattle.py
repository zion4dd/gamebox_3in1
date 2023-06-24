import customtkinter
import tkinter.messagebox
from seabattle_field import GameField
from itertools import product
from random import choice
from time import sleep
from config import get_ico, DEV  # devmod: show droid ships


SIZE = 10


class App(customtkinter.CTk):
    def __init__(self, field_human: GameField, field_droid: GameField, size=10):
        super().__init__()
        customtkinter.set_default_color_theme("blue")

        self.f_human = field_human
        self.f_droid = field_droid
        self._size = size

        self.title("SEABATTLE")
        self.icofile = 'seabattle.ico'
        self.resizable(False, False)
        self.geometry("+400+110")
        get_ico(self)
        self.get_fields()

        # ============ create frames (2x3) ============
        self.frame_left_0 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_left_0.grid(row=0, column=0, padx=10, pady=10)

        self.frame_right_0 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right_0.grid(row=0, column=1, padx=10, pady=10)

        self.frame_left_1 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_left_1.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)

        self.frame_right_1 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right_1.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)

        self.frame_left_2 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_left_2.grid(row=2, column=0, padx=10, pady=10)

        self.frame_right_2 = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right_2.grid(row=2, column=1, padx=10, pady=10)

        # ============ frame_left_0 ============
        self.progressbar_left = customtkinter.CTkProgressBar(master=self.frame_left_0)
        self.progressbar_left.grid()

        # ============ frame_right_0 ============
        self.progressbar_right = customtkinter.CTkProgressBar(master=self.frame_right_0)
        self.progressbar_right.grid()

        # ============ frame_left_1 ============
        self.field_left = [[0] * self._size for _ in range(self._size)]
        for r in range(self._size):
            for c in range(self._size):
                self.field_left[r][c] = customtkinter.CTkButton(master=self.frame_left_1,
                                                text='',
                                                width=28,
                                                border_color='white',
                                                hover=False,
                                                fg_color=self.cell_view_human(r, c))
                self.field_left[r][c].grid(row=r, column=c)

        # ============ frame_right_1 ============
        self.field_right = [[0] * self._size for _ in range(self._size)]
        for r in range(self._size):
            for c in range(self._size):
                self.field_right[r][c] = customtkinter.CTkButton(master=self.frame_right_1,
                                text='',
                                width=28,
                                hover=False,
                                command=lambda row=r, column=c: self.human(row, column))
                self.field_right[r][c].grid(row=r, column=c)

        # ============ frame_left_2 ============
        self.switch = customtkinter.CTkSwitch(master=self.frame_left_2,
                                              text='IQ 70/90')
        self.switch.grid()

        # ============ frame_right_2 ============
        self.button = customtkinter.CTkButton(master=self.frame_right_2,
                                              text='New Game',
                                              command=self.restart)
        self.button.grid()

        self.init()

    def init(self):
        self.fire_cells = [(r, c) for r in range(self._size) for c in range(self._size)] # droids fire cells
        self.fire_next = set() # if droid damage ship
        self.fire_memory = set() # droid hit memory

        self.progressbar_left.set(self.f_human._life / 20)
        self.progressbar_right.set(self.f_droid._life / 20)
        self.switch.select()
        self.get_fields()
    
    def get_fields(self):
        "get fields as 2d list"
        self.f_human_get: list = self.f_human.get_field()
        self.f_droid_get: list = self.f_droid.get_field()

    def cell_view_human(self, r, c):
        match self.f_human_get[r][c]:
            case 0: return ["#3B8ED0", "#1F6AA5"]
            case 1: return 'grey'
            case 2: return 'red'
            case 3: return 'black'
        
    def cell_view_droid(self, r, c):
        match self.f_droid_get[r][c]:
            case 0: return ["#3B8ED0", "#1F6AA5"]
            case 1: return ["#3B8ED0", "#1F6AA5"] if not DEV else 'grey'
            case 2: return 'red'
            case 3: return 'black'

    def redraw(self):
        "redraw field"
        for r in range(self._size):
            for c in range(self._size):
                self.field_left[r][c].configure(fg_color=self.cell_view_human(r, c))
                self.field_right[r][c].configure(fg_color=self.cell_view_droid(r, c))
        self.update()
        
    def flash(self, r, c):
        "shows droids fire"
        sleep(0.7)
        self.field_left[r][c].configure(border_width=4, text='+')
        self.update()
        self.field_left[r][c].configure(border_width=0, text='')

    def check_win(self):
        if self.f_human._life == 0:
            self.win('Ooops.. You lose!')
        if self.f_droid._life == 0:
            self.win('Congrats! You win!')

    def win(self, msg):
        global DEV
        DEV = True
        self.redraw()
        DEV = False
        tkinter.messagebox.showinfo(message=msg)
        self.restart()

    def human(self, r, c):
        if self.f_droid_get[r][c] == 1:
            self.f_droid.hit(r, c)
            self.get_fields()
            self.progressbar_right.set(self.f_droid._life / 20)
            self.check_win()
        self.redraw()
        self.droid()
        self.f_droid.move_ships()
        self.f_human.move_ships()
        self.get_fields()
        self.redraw()

    def droid(self):
        if self.fire_next:
            r, c = choice(tuple(self.fire_next))
            self.fire_next.remove((r, c))
        else:
            r, c = choice(self.fire_cells)
        print(r, c) #test
        self.flash(r, c)
        if self.f_human_get[r][c] == 1:
            self.f_human.hit(r, c) # hit changes self.f_human.get_field()[x][y]
            self.get_fields()
            self.progressbar_left.set(self.f_human._life / 20)
            self.check_win()
            self.fire_memory.add((r, c))
            if self.f_human_get[r][c] == 2: # ship damaged
                if self.switch.get():
                    self.droid_iq_90(r, c)
                else:
                    self.droid_iq_70()
            else: # if self.f_human.get_field()[x][y] == 3 ship dead
                """delete ship and around ship cells from fire_cells. clear fire_next and fire_memory"""
                for r, c in self.fire_memory:
                    for i, j in product([-1,0,1], repeat=2):
                        try:
                            self.fire_cells.remove((r + i, c + j))
                        except:
                            continue
                self.fire_next = set()
                self.fire_memory = set()

    def add_fire_next(self, r, c):
        if min(r, c) >= 0 and max(r, c) < self._size and (r, c) in self.fire_cells:
            self.fire_next.add((r, c))

    def droid_iq_90(self, r, c): # smart algorithm with memory
        mem = self.fire_memory
        if len(mem) < 2:
            for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                self.add_fire_next(r + d[0], c + d[1])
        else:
            max_ = max(i[0] for i in mem), max(i[1] for i in mem)
            min_ = min(i[0] for i in mem), min(i[1] for i in mem)
            if max_[0] == min_[0]:
                max_ = max_[0], max_[1] + 1
                min_ = min_[0], min_[1] - 1
            else:
                max_ = max_[0] + 1, max_[1]
                min_ = min_[0] - 1, min_[1]
            self.fire_next = set()
            self.add_fire_next(*max_)
            self.add_fire_next(*min_)
        print(self.fire_next) #test

    def droid_iq_70(self): # stupid algorithm O(n2)
        f_human = self.f_human_get
        for r in range(self._size):
            for c in range(self._size):
                if f_human[r][c] == 2:
                    for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                        self.add_fire_next(r + d[0], c + d[1])
        print(self.fire_next) #test

    def restart(self):
        self.f_human.init()
        self.f_droid.init()
        self.init()
        self.redraw()


def seabattle():
    field_human = GameField(SIZE)
    field_human.init()
    field_droid = GameField(SIZE)
    field_droid.init()
    
    app = App(field_human, field_droid, size=SIZE)
    app.mainloop()


if __name__ == "__main__":
    seabattle()

