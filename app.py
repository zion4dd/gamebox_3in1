import customtkinter
from gamefield import GameField
from random import randint

DEBUG = True
SIZE = 10

class App(customtkinter.CTk):
    def __init__(self, field_human, field_droid, size=10):
        super().__init__()

        self.title("CustomTkinter complex_example.py")
        self.resizable(False, False)
        self.geometry("+70+70")

        self._size = size
        self._fhuman = field_human
        self._fdroid = field_droid

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
                self.field_left[i][j] = customtkinter.CTkButton(
                                    master=self.frame_left,
                                    text='.',
                                    width=28,
                                    fg_color=self.cell_view_human(i, j),
                                    command=lambda row=i, column=j: self.hit(row, column))
                self.field_left[i][j].grid(row=i, column=j)

        # ============ frame_right ============
        self.field_right = [[0] * self._size for _ in range(self._size)]
        for i in range(self._size):
            for j in range(self._size):
                self.field_right[i][j] = customtkinter.CTkButton(
                                    master=self.frame_right,
                                    text='.',
                                    width=28,
                                    fg_color=self.cell_view_droid(i, j),
                                    command=lambda row=i, column=j: self.hit(row, column))
                self.field_right[i][j].grid(row=i, column=j)

    def cell_view_human(self, i, j):
        if self._fhuman.get_field()[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self._fhuman.get_field()[i][j] == 1:
            return 'grey'
        if self._fhuman.get_field()[i][j] == 2:
            return 'red'
        if self._fhuman.get_field()[i][j] == 3:
            return 'black'
        
    def cell_view_droid(self, i, j):
        if self._fdroid.get_field()[i][j] == 0:
            return ["#3B8ED0", "#1F6AA5"]
        if self._fdroid.get_field()[i][j] == 1:
            return 'grey' if DEBUG else ["#3B8ED0", "#1F6AA5"]
        if self._fdroid.get_field()[i][j] == 2:
            return 'red'
        if self._fdroid.get_field()[i][j] == 3:
            return 'black'
        
    def test(self):
        self._fhuman.move_ships()
        self._fdroid.move_ships()
        self._fhuman.show()
        print()
        self._fdroid.show()
        self.redraw()

    def redraw(self):
        for i in range(self._size):
            for j in range(self._size):
                self.field_left[i][j].configure(fg_color=self.cell_view_human(i, j))
                self.field_right[i][j].configure(fg_color=self.cell_view_droid(i, j))

    def hit(self, i, j):
        if self._fdroid.get_field()[i][j] == 1:
            self._fdroid.hit(j, i)
        self.droid()
        self._fhuman.move_ships()
        self._fdroid.move_ships()
        self.redraw()

    def droid(self):
        x = randint(0, self._size - 1)
        y = randint(0, self._size - 1)
        print(x, y)
        if self._fhuman.get_field()[x][y] == 1:
            self._fhuman.hit(y, x)
        

if __name__ == "__main__":
    print('go')
    field_human = GameField(SIZE)
    field_human.init()
    field_droid = GameField(SIZE)
    field_droid.init()

    app = App(field_human, field_droid, size=SIZE)
    app.mainloop()

