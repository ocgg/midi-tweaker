import rtmidi
import tkinter as tk
import tkinter.ttk as ttk
import src.menus
import src.midi_port


class ApplicationWindow(tk.Tk): # inherits from tk.Tk
    def __init__(self):
        # Call parent class constructor to have its behavior & state under self
        tk.Tk.__init__(self)
        self.midi = rtmidi.MidiIn()
        self.midi_ports = self.midi.get_ports()
        self.geometry("640x480")
        self.title("MIDI Tweaker")

        # LAYOUT ##########
        # Application menu
        self.menu_bar = src.menus.MenuBar(self)
        self.config(menu=self.menu_bar)
        # Main window
        self.main = ttk.Notebook(self)
        self.main.pack(fill='both', expand=True)
        # Generic message
        # label = tk.Label(self.main, text="Choose a MIDI port")
        # label.pack(fill='both', expand=True)
        self.mainloop()

    def open_port(self, port_name, port_index):
        tab = src.midi_port.PortTab(self.main, port_name, port_index)
        split_name = port_name.split(':')[1]
        self.main.add(tab, text=split_name)


# Entry point
if __name__ == "__main__":
    window = ApplicationWindow()
