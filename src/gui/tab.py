import tkinter.ttk as ttk
from src.gui.rule_form_frame import RuleFormFrame
from src.gui.rules_list_frame import RulesListFrame
from src.router.router import Router


class Tab(ttk.Frame):
    def __init__(self, master, port_name):
        super().__init__(master)

        # Router is what links the GUI with the midi port & rules.
        # A tab has one router,
        # which has one midi in port, many rules & one midi out port
        self.ROUTER = Router(self, port_name)

        # MIDI IN bar
        self.midi_in_label = self.__create_midi_bar('IN')
        # MAIN CONTENT:
        # toggle between rules_list_frame and rule_form_frame
        self.rules_list_frame = RulesListFrame(self)
        self.rule_form_frame = RuleFormFrame(self, self.ROUTER)
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

    # PRIVATE METHODS #########################################################

    def __create_midi_bar(self, source):
        midi_label = ttk.Label(
            self,
            text=f"MIDI {source}: Waiting for messages...",
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
