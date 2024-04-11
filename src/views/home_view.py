import tkinter.ttk as ttk


class HomeView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ttk.Label(self, text="Open a MIDI port to start...")
        self.label.pack(fill='both', expand=True)
