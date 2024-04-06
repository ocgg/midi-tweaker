import mido
from tkinter import messagebox
from .rule import Rule


# Router is the rules controller for one Tab.
class TabRouter:
    def __init__(self, tab, port_name):
        self.TAB = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.callback = self._midi_in_callback
        self.midi_out = mido.open_output(f'TWEAKED {port_name}', virtual=True)
        self.rules = []

    def add_rule(self, in_msg_inputs, out_msg_inputs):
        rule = Rule(in_msg_inputs, out_msg_inputs)
        self.rules.append(rule)

    # MIDI CONNECTIONS ########################################################

    def _midi_in_callback(self, msg, data=None):
        in_msg = msg.copy()
        # Apply the rules
        for rule in self.rules:
            msg = rule.translate(msg)
        # Send the message to midi out
        self.midi_out.send(msg)
        # Display the message in the GUI
        self.TAB.midi_in_label.configure(text=f"MIDI_IN: {str(in_msg)}")
        # Display the message in the GUI
        self.TAB.midi_out_label.configure(text=f"MIDI_OUT: {str(msg)}")

    def _open_midi_in(self, port_name):
        try:
            return mido.open_input(port_name)
        except IOError:
            messagebox.showerror("Error", "MIDI port not found")
