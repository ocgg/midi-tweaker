import rtmidi
import rtmidi.midiconstants as consts
from tkinter import messagebox
# from src.router.midi_msg import MidiMsg


# Router is what links the GUI with the midi port & rules.
# A tab has one router,
# which has one midi in port, many rules & one midi out port
class Router:
    def __init__(self, tab, port_name):
        self.TAB = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.set_callback(self.midi_in_callback)
        self.rules = []

    def add_rule(self, rule):
        pass

    def midi_in_callback(self, msg, data=None):
        # Convert msg to MidiMsg object
        # midi_msg = MidiMsg(msg)
        # 1.display midi in message (tab)
        # 2. apply rules & send to midi out
        prefix = "MIDI IN:\n"
        msg_data = msg[0]
        channel = msg_data[0] & 0xF     # lower 4 bits
        msg_type = msg_data[0] & 0xF0   # upper 4 bits

        if msg_type == consts.NOTE_ON:  # Note on
            txt = f"NOTEON CH:{channel} NOTE:{msg_data[1]} VEL:{msg_data[2]}"
        elif msg_type == consts.NOTE_OFF:   # Note off
            txt = f"NOTEOFF CH:{channel} NOTE:{msg_data[1]} VEL:{msg_data[2]}"
        elif msg_type == consts.CONTROL_CHANGE:  # CC
            txt = f"CONTROL CHANGE CH:{channel} CONTROLLER:{msg_data[1]} VAL:{msg_data[2]}"
            # TODO: handle pitch bend & other General Midi specific messages
        else:
            txt = f"Not covered yet: {msg}"
        self.TAB.midi_in_label.configure(text=prefix + txt)

    # PRIVATE METHODS #########################################################

    def _open_midi_in(self, port_name):
        ports = rtmidi.MidiIn().get_ports()
        try:
            port = next(i for i, port in enumerate(ports)
                        if port == port_name)
            return rtmidi.MidiIn().open_port(port)
        except StopIteration:
            messagebox.showerror("Error", "MIDI port not found")
