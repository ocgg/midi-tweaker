import tkinter as tk


class MenuBar:
    def __init__(self, master):
        self.master = master
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Menu File
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Reset")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Menu MIDI ports
        ports_menu = tk.Menu(self.menu_bar, tearoff=0)
        for i, port in enumerate(self.master.midi_ports):
            ports_menu.add_checkbutton(label=f"{i} - {port}", command=lambda: self.select_port(i))
        self.menu_bar.add_cascade(label="MIDI Ports", menu=ports_menu)

    def select_port(self, port):
        print(f"Port selected: {port}")
