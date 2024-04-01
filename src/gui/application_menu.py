import mido
import tkinter as tk


class ApplicationMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.APP_WINDOW = master

        # Menu File
        self.file_menu = tk.Menu(self, tearoff=0)
        self._build_file_menu()

        # Menu MIDI ports
        self.ports_menu = tk.Menu(self, tearoff=0)
        self._build_midi_port_menu()

    # PRIVATE METHODS ##########

    def _build_file_menu(self):
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Reset")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.APP_WINDOW.quit)
        self.add_cascade(label="File", menu=self.file_menu)

    def _ports_menu_has_entries(self):
        try:
            self.ports_menu.index(0)
            return True
        except tk.TclError:
            return False

    def _build_midi_port_menu(self):
        # Delete menu entries
        if self._ports_menu_has_entries():
            self.ports_menu.delete(0, 'end')
        # Get MIDI ports
        midi_ports = mido.get_input_names()
        # Create menu entries
        for i, port in enumerate(midi_ports):
            self.ports_menu.add_command(
                label=f"{i} - {port}",
                command=lambda i=i, port=port:
                    self.APP_WINDOW.MAIN_FRAME.create_tab(port, i))
        self.ports_menu.add_separator()
        self.ports_menu.add_command(
            label="Refresh",
            command=self._build_midi_port_menu)
        self.add_cascade(label="Open MIDI Port", menu=self.ports_menu)
