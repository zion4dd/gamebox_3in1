import customtkinter
import tkinter.messagebox
from tictactoe_field import GameField
import os, sys


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")

DEV = False

class App(customtkinter.CTk):
    def __init__(self, gamefield):
        super().__init__()

        self.title("TICTACTOE")
        self.icofile = 'tictactoe.ico'

        self.resizable(False, False)
        self.geometry("+400+70")

        self.game = gamefield

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(padx=30, pady=30)

        self.field = [[0] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.field[i][j] = customtkinter.CTkButton(master=self.frame,
                                text=self.cell_value(i, j),
                                width=70,
                                height=70,
                                font=('Verdana', 30),
                                command=lambda row=i, column=j: self.go(row, column))
                self.field[i][j].grid(row=i, column=j)

        self.get_ico()

    def get_ico(self):
        try:
            if DEV:
                self.iconbitmap(default=self.icofile)
                return
            
            path = os.path.join(sys._MEIPASS, self.icofile)
            self.iconbitmap(default=path)
        except:
            pass

    def cell_value(self, r, c):
        if self.game[r, c] == 0:
            return ''
        if self.game[r, c] == 1:
            return 'X'
        if self.game[r, c] == 2:
            return 'O'

    def redraw(self):
        for i in range(3):
            for j in range(3):
                self.field[i][j].configure(text=self.cell_value(i, j))
        self.update()
    
    def go(self, r, c):
        if self.game.human(r, c):
            if self.check_win():
                self.game.droid()
                self.check_win()

    def check_win(self):
        self.redraw()
        match self.game.win:
            case 0: return True
            case 1: tkinter.messagebox.showinfo(message='Human WIN!')
            case 2: tkinter.messagebox.showinfo(message='Droid WIN!')
            case 3: tkinter.messagebox.showinfo(message='DRAW!')
        self.restart()

    def restart(self):
        self.game.init()
        self.redraw()


def tictactoe():
    game = GameField()
    game.init()

    app = App(game)
    app.mainloop()


if __name__ == "__main__":
    tictactoe()

