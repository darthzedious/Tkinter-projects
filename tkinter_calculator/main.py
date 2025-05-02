from tkinter import *
from tkinter_calculator.interface import create_interface
from tkinter_calculator.keybinging import on_keypress, bind_keys

root = Tk()
root.geometry("500x270")
root.title("Calculator")
root.resizable(width=False, height=False)

window, frame = create_interface(root)

bind_keys(root, window)


root.mainloop()