import tkinter as tk


class Root(tk.Tk):  # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        super().__init__()

        # Window size : 800x600, position : 100, 100
        self.geometry("800x600+100+100")
        self.minsize(width=200, height=100)

        self.title("MIDI Tweaker")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
