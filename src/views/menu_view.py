import tkinter as tk


class MenuView(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # "File" menu
        self.file_menu = tk.Menu(self, tearoff=0)
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Reset")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit")
        self.add_cascade(label="File", menu=self.file_menu)

        # "MIDI ports" menu
        self.ports_menu = tk.Menu(self, tearoff=0)
        self.ports_menu.add_command(label="Refresh")
        self.ports_menu.add_separator()
        self.add_cascade(label="MIDI ports", menu=self.ports_menu)

    # Called from controller
    def build_ports_menu(self, ports):
        for port in ports:
            self.ports_menu.add_command(label=port)
