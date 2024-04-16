import mido
from tkinter import messagebox


# Router is the rules controller for one Tab.
class TabRouter:
    CHANNEL_VOICE_TYPES = ['note_on', 'note_off', 'control_change',
                           'program_change', 'channel_pressure', 'pitchwheel']

    def __init__(self, tab, port_name):
        self.tab_view = tab
        self.midi_in = None
        self.midi_out = None
        self.rules = []
        self.learn_is_active = False

    def add_rule(self, rule):
        self.rules.append(rule)

    # MIDI CALLBACK ###########################################################

    def _midi_in_callback(self, msg, data=None):
        if msg.type not in self.CHANNEL_VOICE_TYPES:
            text = f"Message type not implemented: {msg.type}"
            self.tab_view.display_midi_msg('MIDI IN', text)

        new_msg = msg.copy()
        # Apply the rules
        for rule in self.rules:
            # Rule applies only if it applies with the original message
            if rule.apply_to(msg):
                new_msg = rule.translate(new_msg)

        if self.midi_out:
            self.midi_out.send(new_msg)
            self.tab_view.display_midi_msg('out', new_msg)
        self.tab_view.display_midi_msg('in', msg)

    # MIDI PORTS ##############################################################

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
            messagebox.showerror("Error", f"MIDI port not found: {port_name}")

    def _set_output_port(self, port_name):
        if self.midi_out:
            self.midi_out.close()
        try:
            self.midi_out = mido.open_output(port_name)
        except IOError:
            messagebox.showerror("Error", f"MIDI port not found: {port_name}")

    # MIDI LEARN ##############################################################

    def learn(self, source):
        if not self.midi_in:
            messagebox.showerror("Error", "No MIDI input port selected")
            return

        if source == 'in':
            form_frame = self.tab_view.frames['form'].in_form
        elif source == 'out':
            form_frame = self.tab_view.frames['form'].out_form

        self.midi_in.callback = lambda msg: self._midi_learn_callback(
            msg, form_frame)
        self.learn_is_active = True
        form_frame.set_learn_btn_active()

    def stop_learn(self, source):
        if source == 'in':
            form_frame = self.tab_view.frames['form'].in_form
        elif source == 'out':
            form_frame = self.tab_view.frames['form'].out_form

        self.midi_in.callback = self._midi_in_callback
        self.learn_is_active = False
        form_frame.set_learn_btn_normal()

    def _midi_learn_callback(self, msg, form_frame):
        form_frame.set_form_state(msg)
