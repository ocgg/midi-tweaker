import mido
from tkinter import messagebox


# Router is what links the GUI with the midi port & rules.
# A tab has one router,
# which has one midi in port, many rules & one midi out port
class Router:
    def __init__(self, tab, port_name):
        self.TAB = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.callback = self.midi_in_callback
        self.rules = []

    def add_rule(self, rule):
        pass

    def midi_in_callback(self, msg, data=None):
        prefix = "MIDI IN:\n"
        self.TAB.midi_in_label.configure(text=prefix + str(msg))

    # PRIVATE METHODS #########################################################

    def _open_midi_in(self, port_name):
        try:
            return mido.open_input(port_name)
        except StopIteration:
            messagebox.showerror("Error", "MIDI port not found")
