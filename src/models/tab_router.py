import mido
from tkinter import messagebox
from .rule import Rule


# Router is the rules controller for one Tab.
class TabRouter:
    CHANNEL_VOICE_TYPES = ['note_on', 'note_off', 'control_change',
                           'program_change', 'channel_pressure', 'pitchwheel']

    def __init__(self, tab, port_name):
        self.tab_view = tab
        self.midi_in = None
        self.midi_out = None
        # self.midi_in = self.set_input_port(port_name)
        # self.midi_in.callback = self._midi_in_callback
        # self.midi_out = mido.open_output(f'TWEAKED {port_name}', virtual=True)
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

        if self.midi_out:
            self.midi_out.send(new_msg)
            self.tab_view.display_midi_msg('out', new_msg)
        self.tab_view.display_midi_msg('in', msg)

    def get_midi_ports(self, source):
        if source == 'in':
            return mido.get_input_names()
        elif source == 'out':
            return mido.get_output_names()

    def set_midi_port(self, event, source, port_name):
        if source == 'in':
            self._set_input_port(port_name)
        elif source == 'out':
            self._set_output_port(port_name)

    def _set_input_port(self, port_name):
        if self.midi_in:
            self.midi_in.close()
        try:
            self.midi_in = mido.open_input(port_name)
            self.midi_in.callback = self._midi_in_callback
        except IOError:
            messagebox.showerror("Error", "MIDI port not found")

    def _set_output_port(self, port_name):
        if self.midi_out:
            self.midi_out.close()
        try:
            self.midi_out = mido.open_output(port_name)
        except IOError:
            messagebox.showerror("Error", f"MIDI port not found: {port_name}")
