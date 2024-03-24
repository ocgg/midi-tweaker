import tkinter as tk
import tkinter.ttk as ttk

class PortTab(ttk.Frame):
    def __init__(self, master, midi, port_name, port_index):
        super().__init__(master)
        self.midi_in = midi.open_port(port_index)
        self.pack(fill='both', expand=True)

        # MIDI IN bar
        self.midi_in_bar = tk.Frame(self, height=50, bg='lightblue')
        self.midi_in_bar.pack(fill='x')
        self.midi_in_msg = ttk.Label(self.midi_in_bar, text="MIDI IN")
        self.midi_in_msg.pack(fill='both', expand=1)

        self.midi_in.set_callback(self.midi_in_callback)

        # Main frame
        self.main = tk.Frame(self)
        self.main.pack(fill='both', expand=True)

        # MIDI OUT bar
        self.midi_out_bar = tk.Frame(self, height=50, bg='lightblue')
        self.midi_out_bar.pack(fill='x')

    def midi_in_callback(self, msg, data=None):
        self.midi_in_msg.configure(text=msg)
