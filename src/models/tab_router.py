import mido
from tkinter import messagebox
from .rule import Rule


# Router is the rules controller for one Tab.
class TabRouter:
    CHANNEL_VOICE_TYPES = ['note_on', 'note_off', 'control_change',
                           'program_change', 'channel_pressure', 'pitchwheel']

    def __init__(self, tab, port_name):
        self.tab_view = tab
        self.midi_in = self._open_midi_in(port_name)
        self.midi_in.callback = self._midi_in_callback
        self.midi_out = mido.open_output(f'TWEAKED {port_name}', virtual=True)
        self.rules = []

    def add_rule(self, in_msg_inputs, out_msg_inputs):
        rule = Rule(in_msg_inputs, out_msg_inputs)
        self.rules.append(rule)

    # MIDI CONNECTIONS ########################################################

    def _midi_in_callback(self, msg, data=None):
        if msg.type not in self.CHANNEL_VOICE_TYPES:
            text = f"Message type not implemented: {msg.type}"
            self.tab_view.display_midi_msg('MIDI IN', text)

        new_msg = msg.copy()
        # Apply the rules
        for rule in self.rules:
            # Rule applies only if it applies with the original message too
            if rule.apply_to(new_msg) and rule.apply_to(msg):
                new_msg = rule.translate(new_msg)
        self.midi_out.send(new_msg)
        # Display message in the GUI
        self.tab_view.display_midi_msg('in', msg)
        self.tab_view.display_midi_msg('out', new_msg)

    def _open_midi_in(self, port_name):
        try:
            return mido.open_input(port_name)
        except IOError:
            messagebox.showerror("Error", "MIDI port not found")
