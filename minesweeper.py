import customtkinter
import tkinter.messagebox
from minesweeper_field import GameField
from config import get_ico


SIZE = 10
MINES = 10

class App(customtkinter.CTk):
    def __init__(self, gamefield, size=10):
        super().__init__()
        customtkinter.set_default_color_theme("green")

        self.gamefield = gamefield
        self.size = size

        self.title("MINESWEEPER")
        self.icofile = 'minesweeper.ico'

        self.resizable(False, False)
        self.geometry("+400+150")
        get_ico(self)

        self.frame = customtkinter.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, padx=30, pady=20)

        self.frame1 = customtkinter.CTkFrame(master=self)
        self.frame1.grid(row=1, column=0, padx=10, pady=10)

        self.buttons = [[0] * self.size for _ in range(self.size)]
        for r in range(self.size):
            for c in range(self.size):
                self.buttons[r][c] = customtkinter.CTkButton(master=self.frame,
                                                             text=self.cell_value(r, c),
                                                             width=28,
                                                             text_color='black',
                                                             command=lambda row=r, col=c: self.go(row, col))
                self.buttons[r][c].bind('<Button-3>', lambda x, row=r, col=c: self.right_click(row, col))
                self.buttons[r][c].grid(row=r, column=c)

        self.button = customtkinter.CTkButton(master=self.frame1,
                                              text='New Game',
                                              command=self.restart)
        self.button.grid()

    def cell_value(self, r, c):
        cell = self.gamefield[r, c]
        if cell.is_open:
            return cell.around_mines if not cell.mine else 'x'
        return ''

    def redraw(self, open_all=False, paint_to_green=False):
        for r in range(self.size):
            for c in range(self.size):
                if open_all:
                    self.gamefield[r, c].is_open = True
                if paint_to_green:
                    self.paint_to_green(r, c)
                self.buttons[r][c].configure(text=self.cell_value(r, c))
        self.update()

    def right_click(self, r, c):
        if self.buttons[r][c].cget('fg_color') == 'red':
            self.paint_to_green(r, c)
        else:
            self.paint_to_red(r, c)

    def paint_to_green(self, r, c):
        self.buttons[r][c].configure(fg_color=['#2CC985', '#2FA572'], hover_color=['#0C955A', '#106A43'])

    def paint_to_red(self, r, c):
        self.buttons[r][c].configure(fg_color='red', hover_color=["#A50021", "#A50021"])

    def go(self, r, c):
        cell = self.gamefield[r, c]
        if cell.mine:
            print('boom')
            self.redraw(open_all=True)
            tkinter.messagebox.showinfo(message='BOOM!')
            self.restart()
        else:
            if cell.around_mines:
                cell.is_open = True
            else:
                self.zerocell(r, c)
            self.redraw()
            self.check_win()

    def zerocell(self, r, c):
        for i in range(r-1, r+2):
            if 0 <= i < self.size:
                for j in range(c-1, c+2):
                    if 0 <= j < self.size:
                        self.gamefield[i, j].is_open = True

    def check_win(self):
        if self.gamefield.win():
            tkinter.messagebox.showinfo(message='Congrats! You win!')
            self.restart()

    def restart(self):
        self.gamefield.init()
        self.redraw(paint_to_green=True)

def minesweeper():
    game = GameField(SIZE, MINES)
    game.init()

    app = App(game, size=SIZE)
    app.mainloop()


if __name__ == "__main__":
    minesweeper()

    