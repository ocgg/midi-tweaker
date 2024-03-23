import rtmidi
import tkinter as tk
import src.menus


class TkWindow(tk.Tk): # inherits from tk.Tk
    def __init__(self, midi_ports):
        # Call parent class constructor to have its behavior & state under self
        tk.Tk.__init__(self)
        self.midi_ports = midi_ports
        self.geometry("640x480")
        self.title("MIDI Tweaker")

        # LAYOUT ##########
        # Application menu
        self.menu_bar = src.menus.MenuBar(self)
        # MIDI IN bar
        self.midi_in = tk.Frame(self, height=50, bg='lightblue')
        self.midi_in.pack(fill='x')
        # Main window
        self.main = tk.Frame(self)
        self.main.pack(fill='both', expand=True)
        # MIDI OUT bar
        self.midi_out = tk.Frame(self, height=50, bg='lightblue')
        self.midi_out.pack(fill='x')

        # Generic message
        label = tk.Label(self.main, text="Choose a MIDI port")
        label.pack(fill='both', expand=True)


# Entry point
if __name__ == "__main__":
    midi = rtmidi.MidiIn()
    midi_ports = midi.get_ports()
    window = TkWindow(midi_ports)
    window.mainloop()
