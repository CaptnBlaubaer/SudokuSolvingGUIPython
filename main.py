import tkinter as tk
from applicationParts import GUI, EventHandler

window = tk.Tk()

window.title("Sudoku Solving machine")

gui = GUI()

eventHandler = EventHandler(gui)

window.mainloop()



