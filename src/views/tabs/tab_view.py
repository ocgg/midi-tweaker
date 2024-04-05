import tkinter.ttk as ttk
from .rules_list_view import RulesListView
from .rule_form_view import RuleFormView


class TabView(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.main_frame = main_frame

        self.frames = {}

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        midi_label_options = {'padx': 10, 'pady': 10, 'sticky': 'w'}

        # MIDI IN bar
        self.midi_in_label = self._create_midi_bar('IN')
        self.midi_in_label.grid(row=0, **midi_label_options)

        ttk.Separator(self, orient='horizontal').grid(row=1, sticky='ew')

        # MAIN CONTENT:
        self._add_frame('form', RuleFormView)
        self._add_frame('list', RulesListView)

        ttk.Separator(self, orient='horizontal').grid(row=3, sticky='ew')

        # MIDI OUT bar
        self.midi_out_label = self._create_midi_bar('OUT')
        self.midi_out_label.grid(row=4, **midi_label_options)

    # DISPLAYING ##############################################################

    def display_rule_form(self):
        self.frames['form'].lift()

    def display_rules_list(self):
        self.frames['list'].lift()

    # PRIVATE #################################################################

    def _add_frame(self, name, Frame):
        self.frames[name] = Frame(self)
        self.frames[name].grid(row=2, sticky="nsew")

    def _create_midi_bar(self, source):
        return ttk.Label(self, text=f"MIDI {source}: Waiting for messages...")
