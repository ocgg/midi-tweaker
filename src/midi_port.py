import rtmidi
import tkinter as tk
import tkinter.ttk as ttk

class PortTab(ttk.Frame):
    def __init__(self, master, port_name, port_index):
        super().__init__(master)
        midi = rtmidi.MidiIn()
        self.midi_in = midi.open_port(port_index)
        self.midi_in.set_callback(self.midi_in_callback)

        # Main frame
        self.main = tk.Frame(self)

        # MIDI IN bar
        self.midi_in_bar = tk.Frame(self)
        self.midi_in_label = ttk.Label(
            self.midi_in_bar,
            text="MIDI IN: waiting for messages...",
            anchor='w',
            width=50
        )
        self.midi_in_label.pack(fill='x')
        midi_in_separator = ttk.Separator(self.midi_in_bar, orient='horizontal')
        midi_in_separator.pack(fill='x')

        # MIDI OUT bar
        self.midi_out_bar = tk.Frame(self, height=50, bg='lightblue')
        self.midi_out_label = ttk.Label(
            self.midi_out_bar,
            text="MIDI OUT: waiting for messages...",
            anchor='w',
            width=50
        )
        midi_out_separator = ttk.Separator(self.midi_out_bar, orient='horizontal')
        midi_out_separator.pack(fill='x')
        self.midi_out_label.pack(fill='x')

        # PACKING (layout) ##########
        self.midi_in_bar.pack(fill='x')
        self.main.pack(fill='both', expand=True)
        self.midi_out_bar.pack(fill='x')
        self.pack(fill='both', expand=True)

    def midi_in_callback(self, msg, data=None):
        prefix = "MIDI IN: "
        msg_data = msg[0]
        channel = msg_data[0] & 0xF
        msg_type = msg_data[0] & 0xF0

        if msg_type == 0x90:  # Note on
            txt = f"CH: {channel}   | NOTEON  {msg_data[1]}     | VEL: {msg_data[2]}"
        elif msg_type == 0x80:    # Note off
            txt = f"CH: {channel}   | NOTEOFF {msg_data[1]}     | VEL: {msg_data[2]}"
        elif msg_type == 0xB0:  # CC
            txt = f"CH: {channel}   | CC    {msg_data[1]}       | VAL: {msg_data[2]}"
        self.midi_in_label.configure(text=prefix + txt)
