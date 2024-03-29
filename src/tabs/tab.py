import rtmidi
import rtmidi.midiconstants as consts
import tkinter as tk
import tkinter.ttk as ttk
import src.tabs.rule_form_frame as rule_form_frame
import src.tabs.rules_list_frame as rules_list_frame


###############################################################################
# Tab is the main router class for CRUD of Rule model                         #
# It manages the display of rules_list_frame & rule_form_frame                #
# And send actions to rules_controller                                        #
###############################################################################
class Tab(ttk.Frame):
    def __init__(self, master, port_name, port_index):
        super().__init__(master)

        midi = rtmidi.MidiIn()
        self.midi_in = midi.open_port(port_index)
        self.midi_in.set_callback(self.midi_in_callback)

        # MIDI IN bar
        self.midi_in_label = self.__create_midi_bar('IN')

        # MAIN CONTENT:
        # must toggle between rules_list_frame and rule_form_frame
        self.rules_list_frame = rules_list_frame.RulesListFrame(self)
        self.rule_form_frame = rule_form_frame.RuleFormFrame(self)

        # MIDI OUT bar
        self.midi_out_label = self.__create_midi_bar('OUT')

        # Pack all widgets
        self.__packer()

    def display_rule_form(self):
        self.rules_list_frame.grid_forget()
        self.rule_form_frame.grid(row=2)

    def display_rules_list(self):
        self.rule_form_frame.grid_forget()
        self.rules_list_frame.grid(row=2)

    def midi_in_callback(self, msg, data=None):
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
        self.midi_in_label.configure(text=prefix + txt)

    def __create_midi_bar(self, source):
        midi_label = ttk.Label(
            self,
            text=f"MIDI {source}:\nWaiting for messages...",
            anchor='w',
            width=50)
        return midi_label

    def __packer(self):
        midi_label_options = {'padx': 10, 'pady': 10}
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.midi_in_label.grid(row=0, **midi_label_options)
        ttk.Separator(self, orient='horizontal').grid(row=1, sticky='ew')
        self.rules_list_frame.grid(row=2)
        ttk.Separator(self, orient='horizontal').grid(row=3, sticky='ew')
        self.midi_out_label.grid(row=4, **midi_label_options)
        self.pack(fill='both', expand=True)
