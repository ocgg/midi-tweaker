import tkinter as tk


class Root(tk.Tk):  # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        super().__init__()

        self.geometry("640x480")
        self.minsize(width=200, height=100)

        self.title("MIDI Tweaker")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
