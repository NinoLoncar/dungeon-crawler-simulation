from game import Game
from game_ui import GameUi
import tkinter as tk

root = tk.Tk()
game = Game()
game.ui = GameUi(root, game)
root.mainloop()
