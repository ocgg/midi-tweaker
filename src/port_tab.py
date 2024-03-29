import rtmidi
import rtmidi.midiconstants as consts
import tkinter as tk
import tkinter.ttk as ttk
# import src.rule


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
        self.add_rule_btn = tk.Button(
            self.main,
            text='Add Rule',
            command=self.new_rule)
        # MIDI OUT bar
        self.midi_out_label = self.create_midi_bar('OUT')

        # PACKING
        self.packer()

    def new_rule(self):
        self.add_rule_btn.pack_forget()
        self.rule_frame = tk.Frame(self.main)
        tk.Label(self.rule_frame, text='Route message:').grid(row=0, column=0, columnspan=4)
        tk.Label(self.rule_frame, text='CH:').grid(row=1, column=0)
        in_ch = ttk.Combobox(self.rule_frame, values=[i for i in range(1, 17)], width=3)
        in_ch.grid(row=1, column=1)
        tk.Label(self.rule_frame, text='NOTE:').grid(row=1, column=2)
        in_note = ttk.Combobox(self.rule_frame, values=[i for i in range(1, 129)], width=5)
        in_note.grid(row=1, column=3)
        tk.Label(self.rule_frame, text='To:').grid(row=2, column=0, columnspan=4)
        tk.Label(self.rule_frame, text='CH:').grid(row=3, column=0)
        out_ch = ttk.Combobox(self.rule_frame, values=[i for i in range(1, 17)], width=3)
        out_ch.grid(row=3, column=1)
        tk.Label(self.rule_frame, text='NOTE:').grid(row=3, column=2)
        out_note = ttk.Combobox(self.rule_frame, values=[i for i in range(1, 129)], width=5)
        out_note.grid(row=3, column=3)
        tk.Button(self.rule_frame, text='OK', command=lambda: self.add_rule(in_ch.get(), in_note.get(), out_ch.get(), out_note.get())).grid(row=4, column=0, columnspan=4)
        self.rule_frame.pack()

    # TODO: This method must be in a repo class
    def add_rule(self, in_ch, in_note, out_ch, out_note):
        # pack_forget before destroy avoid little glitch
        self.rule_frame.pack_forget()
        self.rule_frame.destroy()
        frame = tk.Frame(self.main)
        tk.Label(frame, text=f"Route {in_ch}:{in_note} to {out_ch}:{out_note}").pack()
        frame.pack()

    def midi_in_callback(self, msg, data=None):
        prefix = "MIDI IN:\n"
        msg_data = msg[0]
        channel = msg_data[0] & 0xF     # lower 4 bits
        msg_type = msg_data[0] & 0xF0   # upper 4 bits

        if msg_type == consts.NOTE_ON:  # Note on
            txt = f"NOTEON | CH: {channel} | NOTE: {msg_data[1]} | VEL: {msg_data[2]}"
        elif msg_type == consts.NOTE_OFF:    # Note off
            txt = f"NOTEOFF | CH: {channel} | NOTE: {msg_data[1]} | VEL: {msg_data[2]}"
        elif msg_type == consts.CONTROL_CHANGE:  # CC
            txt = f"CONTROL CHANGE | CH: {channel} | CONTROLLER: {msg_data[1]} | VAL: {msg_data[2]}"
            # TODO: handle pitch bend & other General Midi specific messages
        else:
            txt = f"Not covered yet: {msg}"
        self.midi_in_label.configure(text=prefix + txt)

    def create_midi_bar(self, source):
        midi_label = ttk.Label(
            self,
            text=f"MIDI {source}:\nWaiting for messages...",
            anchor='w',
            width=50)
        return midi_label

    def packer(self):
        midi_label_options = {'fill': 'x', 'padx': 10, 'pady': 10}

        self.midi_in_label.pack(**midi_label_options)
        self.main.pack(fill='both', expand=True)
        ttk.Separator(self.main, orient='horizontal').pack(side='top', fill='x')
        self.add_rule_btn.pack(expand=True)
        ttk.Separator(self.main, orient='horizontal').pack(side='bottom', fill='x')
        self.midi_out_label.pack(**midi_label_options)
        self.pack(fill='both', expand=True)
