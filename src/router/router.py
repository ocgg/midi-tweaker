import mido
from tkinter import messagebox


# Router is the rules controller for one Tab.
# And it is what links the GUI with the midi port.
class Router:
    def __init__(self, tab, port_name):
        self.TAB = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.callback = self._midi_in_callback
        self.midi_out = mido.open_output('gnah', virtual=True)
        self.rules = []

    def add_rule(self, rule):
        pass

    # PRIVATE METHODS #########################################################

    def _midi_in_callback(self, msg, data=None):
        # Display the message in the GUI
        self.TAB.midi_in_label.configure(text=f"MIDI_IN: {str(msg)}")
        # Apply the rules
        # Send the message to midi out
        self.midi_out.send(msg)
        # Display the message in the GUI
        self.TAB.midi_out_label.configure(text=f"MIDI_OUT: {str(msg)}")

    def _open_midi_in(self, port_name):
        try:
            return mido.open_input(port_name)
        except IOError:
            messagebox.showerror("Error", "MIDI port not found")
