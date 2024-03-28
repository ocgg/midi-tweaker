import tkinter as tk
import tkinter.ttk as ttk
from src.views.port_tab import PortTab


class MainFrame(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)
        # "Welcome" message
        self.first_label = tk.Label(self, text="Open a MIDI port to start...")
        self.first_label.pack(fill='both', expand=True)

    # Called from ApplicationMenu ("Open MIDI Port" menu)
    def create_tab(self, port_name, port_index):
        self.first_label.pack_forget()
        tab = PortTab(
            self,
            port_name,
            port_index)
        split_name = port_name.split(':')[1]
        self.add(tab, text=split_name)
