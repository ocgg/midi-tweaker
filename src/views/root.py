import tkinter as tk
import tkinter.ttk as ttk


class Root(tk.Tk):  # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        super().__init__()

        self.geometry("640x480")
        self.minsize(width=200, height=100)

        self.title("MIDI Tweaker")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.style = ttk.Style()
        # self.style.configure('TLabel', font=('Helvetica', 10))
