import customtkinter
import tkinter.messagebox
from tictactoe_field import TicTacToe


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

DEV = False

class App(customtkinter.CTk):
    def __init__(self, gamefield):
        super().__init__()

        self.title("TICTACTOE")

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
                                command=lambda row=i, column=j: self.human(row, column))
                self.field[i][j].grid(row=i, column=j)

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
    
    def human(self, r, c):
        if self.game.human_go(r, c):
            self.redraw()
            if self.check_win():
                self.game.droid_go()
                self.redraw()
                self.check_win()

    def check_win(self):
        if self.game.is_human_win:
            tkinter.messagebox.showinfo(message='human')
            self.restart()
            return
        if self.game.is_droid_win:
            tkinter.messagebox.showinfo(message='droid')
            self.restart()
            return
        if self.game.is_draw:
            tkinter.messagebox.showinfo(message='draw')
            self.restart()
            return
        return True

    def restart(self):
        self.game.init()
        self.redraw()


def tictactoe():
    game = TicTacToe()
    game.init()
    app = App(game)
    app.mainloop()

if __name__ == "__main__":
    tictactoe()
