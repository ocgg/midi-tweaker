import rtmidi
import tkinter as tk
import tkinter.ttk as ttk

class PortTab(ttk.Frame):
    def __init__(self, master, port_name, port_index):
        super().__init__(master)

        midi = rtmidi.MidiIn()
        self.midi_in = midi.open_port(port_index)
        self.midi_in.set_callback(self.midi_in_callback)

        # MIDI IN bar
        self.midi_in_label = self.create_midi_bar('IN')
        # Main frame
        self.main = tk.Frame(self)
        # MIDI OUT bar
        self.midi_out_label = self.create_midi_bar('OUT')

        # PACKING
        self.packer()

    def midi_in_callback(self, msg, data=None):
        prefix = "MIDI IN: "
        msg_data = msg[0]
        channel = msg_data[0] & 0xF     # lower 4 bits
        msg_type = msg_data[0] & 0xF0   # upper 4 bits

        if msg_type == 0x90:  # Note on
            txt = f"CH: {channel}   | NOTEON  {msg_data[1]}     | VEL: {msg_data[2]}"
        elif msg_type == 0x80:    # Note off
            txt = f"CH: {channel}   | NOTEOFF {msg_data[1]}     | VEL: {msg_data[2]}"
        elif msg_type == 0xB0:  # CC
            txt = f"CH: {channel}   | CC    {msg_data[1]}       | VAL: {msg_data[2]}"
        self.midi_in_label.configure(text=prefix + txt)

    def create_midi_bar(self, source):
        midi_label = ttk.Label(
            self,
            text=f"MIDI {source}: waiting for messages...",
            anchor='w',
            width=50
        )
        return midi_label

    def packer(self):
        midi_label_options = { 'fill': 'x', 'padx': 10, 'pady': 10 }

        self.midi_in_label.pack(**midi_label_options)
        self.main.pack(fill='both', expand=True)
        ttk.Separator(self.main, orient='horizontal').pack(side='top', fill='x')
        ttk.Separator(self.main, orient='horizontal').pack(side='bottom', fill='x')
        self.midi_out_label.pack(**midi_label_options)
        self.pack(fill='both', expand=True)
