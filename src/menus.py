import tkinter as tk


class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Menu File
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Reset")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Menu MIDI ports
        ports_menu = tk.Menu(self, tearoff=0)
        for i, port in enumerate(self.master.midi_ports):
            ports_menu.add_command(
                label = f"{i} - {port}",
                command = lambda i=i, port=port: self.master.open_port(port, i)
            )
        self.add_cascade(label="Open MIDI Ports", menu=ports_menu)
