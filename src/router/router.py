import mido
from tkinter import messagebox
from src.router.rule_model import Rule


# Router is the rules controller for one Tab.
# And it is what links the GUI with the midi port.
class Router:
    def __init__(self, tab, port_name):
        self.TAB = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.callback = self._midi_in_callback
        self.midi_out = mido.open_output(f'TWEAKED {port_name}', virtual=True)
        self.rules = []

    def add_rule(self, from_msg, to_msg):
        rule_attributes = list(from_msg.keys())
        rule = Rule(rule_attributes, from_msg, to_msg)
        self.rules.append(rule)

    # PRIVATE METHODS #########################################################

    def _midi_in_callback(self, msg, data=None):
        # Display the message in the GUI
        self.TAB.midi_in_label.configure(text=f"MIDI_IN: {str(msg)}")
        # Apply the rules
        for rule in self.rules:
            print(rule.apply_to(msg))
            if rule.apply_to(msg):
                msg = rule.translate(msg)
        # Send the message to midi out
        self.midi_out.send(msg)
        # Display the message in the GUI
        self.TAB.midi_out_label.configure(text=f"MIDI_OUT: {str(msg)}")

    def _open_midi_in(self, port_name):
        try:
            return mido.open_input(port_name)
        except IOError:
            messagebox.showerror("Error", "MIDI port not found")
