import tkinter as tk
from src.gui.application_menu import ApplicationMenu
from src.gui.application_main_frame import ApplicationMainFrame


class ApplicationWindow(tk.Tk):  # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        tk.Tk.__init__(self)
        self.geometry("640x480")
        self.title("MIDI Tweaker")

        # LAYOUT ##########
        # Application menu
        self.application_menu = ApplicationMenu(self)
        self.config(menu=self.application_menu)
        # Main frame
        self.MAIN_FRAME = ApplicationMainFrame(self)
        self.MAIN_FRAME.pack(fill='both', expand=True)
