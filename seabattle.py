import customtkinter
import tkinter.messagebox
from seabattle_field import GameField
from itertools import product
from random import choice
from time import sleep
import os, sys


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

DEV = False # devmod: show droid ships; icon = ./icon.ico
SIZE = 10

class App(customtkinter.CTk):
    def __init__(self, field_human: GameField, field_droid: GameField, size=10):
        super().__init__()

        self.title("SEABATTLE")
        self.icofile = 'seabattle.ico'

        self.resizable(False, False)
        self.geometry("+400+70")

        self.f_human = field_human
        self.f_droid = field_droid
        self.f_human_get: list = field_human.get_field() # 2d [[],[]]
        self.f_droid_get: list = field_droid.get_field() # 2d [[],[]]
        
        self._size = size
        self.fire_cells = [(x, y) for x in range(self._size) for y in range(self._size)] # droids fire cells
        self.fire_next = set() # if droid damage ship
        self.fire_memory = set() # droids hit memory

        self.life_human = sum(sum(x) for x in self.f_human_get)
        self.life_droid = sum(sum(x) for x in self.f_droid_get)

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
        for i in range(self._size):
            for j in range(self._size):
                self.field_left[i][j] = customtkinter.CTkButton(master=self.frame_left_1,
                                                                text='',
                                                                width=28,
                                                                border_color='white',
                                                                hover=False,
                                                                fg_color=self.cell_view_human(i, j))
                self.field_left[i][j].grid(row=i, column=j)

        # ============ frame_right_1 ============
        self.field_right = [[0] * self._size for _ in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
                self.field_right[i][j] = customtkinter.CTkButton(master=self.frame_right_1,
                                                                 text='',
                                                                 width=28,
                                                                 hover=False,
                                                                 command=lambda row=i, column=j: self.fire(row, column))
                self.field_right[i][j].grid(row=i, column=j)

        # ============ frame_left_2 ============
        self.switch = customtkinter.CTkSwitch(master=self.frame_left_2,
                                              text='IQ 70/90')
        self.switch.grid()

        # ============ frame_right_2 ============
        self.button = customtkinter.CTkButton(master=self.frame_right_2,
                                              text='New Game',
                                              command=self.restart)
        self.button.grid()

        # ============ set default ============
        self.get_ico()
        self.progressbar_left.set(self.life_human / 20)
        self.progressbar_right.set(self.life_droid / 20)
        self.switch.select()

    def get_ico(self):
        try:
            if DEV:
                self.iconbitmap(default=self.icofile)
                return
            
            path = os.path.join(sys._MEIPASS, self.icofile)
            self.iconbitmap(default=path)
        except:
            pass

    def cell_view_human(self, i, j):
        if self.f_human_get[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self.f_human_get[i][j] == 1:
            return 'grey'
        if self.f_human_get[i][j] == 2:
            return 'red'
        if self.f_human_get[i][j] == 3:
            return 'black'
        
    def cell_view_droid(self, i, j):
        if self.f_droid_get[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self.f_droid_get[i][j] == 1:
            return ["#3B8ED0", "#1F6AA5"] if not DEV else 'grey'
        if self.f_droid_get[i][j] == 2:
            return 'red'
        if self.f_droid_get[i][j] == 3:
            return 'black'

    def redraw(self):
        "redraw field"
        self.f_human_get = self.f_human.get_field()
        self.f_droid_get = self.f_droid.get_field()
        for i in range(self._size):
            for j in range(self._size):
                self.field_left[i][j].configure(fg_color=self.cell_view_human(i, j))
                self.field_right[i][j].configure(fg_color=self.cell_view_droid(i, j))
        self.update()
        
    def flash(self, i, j):
        "shows droids fire"
        sleep(0.5)
        self.field_left[i][j].configure(border_width=4, text='+')
        self.update()
        sleep(0.5)
        self.field_left[i][j].configure(border_width=0, text='')

    def life_reduce(self, victim):
        "reduce life progressbar and checks win"
        global DEV
        if victim == 'human':
            self.life_human -= 1
            self.progressbar_left.set(self.life_human / 20)
            if self.life_human == 0:
                DEV = True
                self.redraw()
                DEV = False
                tkinter.messagebox.showinfo(message='Ooops.. You lose!')
                seabattle()
        if victim == 'droid':
            self.life_droid -= 1
            self.progressbar_right.set(self.life_droid / 20)
            if self.life_droid == 0:
                self.redraw()
                tkinter.messagebox.showinfo(message='Congrats! You win!')
                seabattle()

    def fire(self, i, j):
        if self.f_droid.get_field()[i][j] == 1:
            self.f_droid.hit(i, j)
            self.life_reduce('droid')
        self.redraw()
        self.droid()
        self.f_droid.move_ships()
        self.f_human.move_ships()
        self.redraw()

    def droid(self):
        if self.fire_next:
            x, y = choice(tuple(self.fire_next))
            self.fire_next.remove((x, y))
        else:
            x, y = choice(self.fire_cells)
        print(x, y) #test
        self.flash(x, y)
        if self.f_human.get_field()[x][y] == 1:
            self.f_human.hit(x, y) # hit changes self.f_human.get_field()[x][y]
            self.life_reduce('human')
            self.fire_memory.add((x, y))
            if self.f_human.get_field()[x][y] == 2: # ship damaged
                if self.switch.get():
                    self.droid_iq_90(x, y)
                else:
                    self.droid_iq_70()
            else: # if self.f_human.get_field()[x][y] == 3 ship dead
                """delete ship and around ship cells from fire_cells. clear fire_next and fire_memory"""
                for x, y in self.fire_memory:
                    for a, b in product([-1,0,1], repeat=2):
                        try:
                            self.fire_cells.remove((x + a, y + b))
                        except:
                            continue
                self.fire_next = set()
                self.fire_memory = set()

    def add_fire_next(self, x, y):
        if min(x, y) >= 0 and max(x, y) < self._size and (x, y) in self.fire_cells:
            self.fire_next.add((x, y))

    def droid_iq_90(self, x, y): # smart algorithm with memory
        mem = self.fire_memory
        if len(mem) < 2:
            for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                self.add_fire_next(x + d[0], y + d[1])
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
        fhuman = self.f_human.get_field()
        for x in range(self._size):
            for y in range(self._size):
                if fhuman[x][y] == 2:
                    for d in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                        self.add_fire_next(x + d[0], y + d[1])
        print(self.fire_next) #test

    def restart(self):
        self.destroy()
        seabattle()


def seabattle():
    field_human = GameField(SIZE)
    field_human.init()
    field_droid = GameField(SIZE)
    field_droid.init()
    
    app = App(field_human, field_droid, size=SIZE)
    app.mainloop()


if __name__ == "__main__":
    seabattle()

