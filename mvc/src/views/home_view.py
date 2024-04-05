import tkinter as tk


class HomeView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = tk.Label(self, text="Open a MIDI port to start...")
        self.label.pack(fill='both', expand=True)
