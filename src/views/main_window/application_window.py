import tkinter as tk
import src.views.main_window.application_menu as app_menu
import src.views.main_window.main_frame as main_frame


class ApplicationWindow(tk.Tk):  # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        tk.Tk.__init__(self)
        self.geometry("640x480")
        self.title("MIDI Tweaker")

        # LAYOUT ##########
        # Application menu
        self.application_menu = app_menu.ApplicationMenu(self)
        self.config(menu=self.application_menu)
        # Main frame
        self.MAIN_FRAME = main_frame.MainFrame(self)
        self.MAIN_FRAME.pack(fill='both', expand=True)
