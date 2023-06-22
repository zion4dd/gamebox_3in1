import customtkinter
from tictactoe import tictactoe
from seabattle import seabattle

def minesweeper():
    pass

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GAMEBOX")
        self.geometry("+70+70")

        self.button = customtkinter.CTkButton(master=self, text='TICTACTOE', command=tictactoe)
        self.button.grid(row=0, column=0, padx=50, pady=10)

        self.button = customtkinter.CTkButton(master=self, text='SEABATTLE', command=seabattle)
        self.button.grid(row=1, column=0, padx=50, pady=10)

        self.button = customtkinter.CTkButton(master=self, text='MINESWEEPER', command=minesweeper)
        self.button.grid(row=3, column=0, padx=50, pady=10)

app = App()
app.mainloop()
