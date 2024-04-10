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

        # Add 'Open tab' button
        self.add_command(label="Open tab")
