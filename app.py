import customtkinter
from tictactoe import tictactoe
from seabattle import seabattle
from minesweeper import minesweeper
from config import get_ico


customtkinter.set_appearance_mode("system")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("GAMEBOX")
        self.icofile = 'icon.ico'
        self.resizable(False, False)
        self.geometry("+70+70")
        get_ico(self)

        self.button = customtkinter.CTkButton(master=self,
                                              fg_color=["#DC143C", "#DC143C"],
                                              hover_color=["#A50021", "#A50021"], 
                                              text='TICTACTOE', 
                                              command=tictactoe)
        self.button.grid(row=0, column=0, padx=50, pady=10)

        self.button = customtkinter.CTkButton(master=self, 
                                              text='SEABATTLE', 
                                              command=seabattle)
        self.button.grid(row=1, column=0, padx=50, pady=10)

        self.button = customtkinter.CTkButton(master=self, 
                                              fg_color=['#2CC985', '#2FA572'], 
                                              hover_color=['#0C955A', '#106A43'],
                                              text='MINESWEEPER', 
                                              command=minesweeper)
        self.button.grid(row=3, column=0, padx=50, pady=10)


app = App()
app.mainloop()
