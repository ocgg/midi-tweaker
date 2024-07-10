import mido
from tkinter import messagebox
from src.modules.constants import MIDO_TYPES


# Router is the rules controller for one Tab.
class TabRouter:
    def __init__(self, tab, port_name):
        self.tab_view = tab

        self.midi_in = []
        self.midi_out = None
        self.rules = []
        self.learn_is_active = False

    def add_rule(self, rule):
        self.rules.append(rule)

    # MIDI CALLBACK ###########################################################

    def _midi_in_callback(self, msg, data=None):
        if msg.type not in MIDO_TYPES:
            text = f"Message type not implemented: {msg.type}"
            messagebox.showerror("Error", text)
            return

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

    def _midi_learn_callback(self, msg, form_frame):
        form_frame.set_form_state(msg)

    # MIDI PORTS ##############################################################

    def get_midi_ports(self, source):
        if source == 'in':
            return mido.get_input_names()
        elif source == 'out':
            return mido.get_output_names()

    def close_midi_ports(self, source):
        if source == 'in' and self.midi_in:
            [port.close() for port in self.midi_in]
            self.midi_in = []
        elif source == 'out' and self.midi_out:
            self.midi_out.close()

    def set_input_ports_all(self):
        self.close_midi_ports('in')
        try:
            midi_in_ports = mido.get_input_names()
            for port_name in midi_in_ports:
                port = mido.open_input(port_name)
                self.midi_in.append(port)
                port.callback = self._midi_in_callback
        except IOError:
            text = ("Please refresh input ports and retry. If the error "
                    "persists, try input ports one by one.")
            messagebox.showerror("Error", text)

    def set_midi_port(self, source, port_name):
        self.close_midi_ports(source)
        if source == 'in':
            self._set_input_port(port_name)
        elif source == 'out':
            self._set_output_port(port_name)

    def _set_input_port(self, port_name):
        try:
            self.midi_in = [mido.open_input(port_name)]
            self.midi_in[0].callback = self._midi_in_callback
        except IOError:
            messagebox.showerror("Error", f"MIDI port not found: {port_name}")

    def _set_output_port(self, port_name):
        try:
            self.midi_out = mido.open_output(port_name)
        except IOError:
            messagebox.showerror("Error", f"MIDI port not found: {port_name}")

    def create_virtual_out(self, name):
        try:
            self.midi_out = mido.open_output(name, virtual=True)
            print(self.midi_out)
        except IOError:
            messagebox.showerror("Error", "Could not create output port")

    # MIDI LEARN ##############################################################

    def learn(self, source):
        if not self.midi_in:
            messagebox.showerror("Error", "No MIDI input port selected")
            return

        form_frame = self.tab_view.frames['form'].forms[source]

        for port in self.midi_in:
            port.callback = lambda msg: self._midi_learn_callback(
                msg, form_frame)
        self.learn_is_active = True
        form_frame.set_learn_btn_active()

    def stop_learn(self, source):
        form_frame = self.tab_view.frames['form'].forms[source]

        for port in self.midi_in:
            port.callback = self._midi_in_callback
        self.learn_is_active = False
        form_frame.set_learn_btn_normal()
