import tkinter as tk
import rtmidi


class ApplicationMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        self.APP_WINDOW = master

        # Menu File
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="Open")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Save as...")
        file_menu.add_command(label="Reset")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.APP_WINDOW.quit)
        self.add_cascade(label="File", menu=file_menu)

        # Menu MIDI ports
        self.ports_menu = tk.Menu(self, tearoff=0)
        self.__build_midi_port_menu()
        self.add_cascade(label="Open MIDI Port", menu=self.ports_menu)

    # PRIVATE METHODS ##########

    def __ports_menu_has_entries(self):
        try:
            self.ports_menu.index(0)
            return True
        except tk.TclError:
            return False

    def __build_midi_port_menu(self):
        # Get MIDI ports
        midi = rtmidi.MidiIn()
        midi_ports = midi.get_ports()
        # Delete menu entries
        if self.__ports_menu_has_entries():
            self.ports_menu.delete(0, 'end')
        # Create menu entries
        for i, port in enumerate(midi_ports):
            self.ports_menu.add_command(
                label=f"{i} - {port}",
                command=lambda i=i, port=port:
                    self.APP_WINDOW.MAIN_FRAME.create_tab(port, i))
        self.ports_menu.add_separator()
        self.ports_menu.add_command(
            label="Refresh",
            command=self.__build_midi_port_menu)
