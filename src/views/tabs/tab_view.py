import tkinter as tk
import tkinter.ttk as ttk
from .rules_list_view import RulesListView
from .rule_form_view import RuleFormView


class TabView(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.main_frame = main_frame

        self.frames = {}
        self.midi_labels = {}

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # MIDI IN bar
        midi_in_bar = self._create_midi_bar('in')

        # MAIN CONTENT:
        self.frames['form'] = RuleFormView(self)
        self.frames['list'] = RulesListView(self)

        # MIDI OUT bar
        midi_out_bar = self._create_midi_bar('out')

        # Init
        self.midi_labels['in']['channel']['label'].config(text='CH:')
        self.midi_labels['in']['type']['label'].config(text='TYPE:')
        self.midi_labels['out']['channel']['label'].config(text='CH:')
        self.midi_labels['out']['type']['label'].config(text='TYPE:')

        # LAYOUT
        midi_in_bar.grid(row=0, sticky='ew')
        ttk.Separator(self, orient='horizontal').grid(row=1, sticky='ew')
        self.frames['form'].grid(row=2, sticky="nsew")
        self.frames['list'].grid(row=2, sticky="nsew")
        ttk.Separator(self, orient='horizontal').grid(row=3, sticky='ew')
        midi_out_bar.grid(row=4, sticky='ew')

    # DISPLAYING ##############################################################

    def display_rule_form(self):
        self.frames['form'].lift()

    def display_rules_list(self):
        self.frames['list'].lift()

    def display_midi_msg(self, source, msg):
        labels = self.midi_labels[source]
        labels['type']['value'].config(text=msg.type)
        labels['channel']['value'].config(text=msg.channel)
        match msg.type:
            case 'note_on' | 'note_off':
                labels['val_1']['label'].config(text='NOTE:')
                labels['val_2']['label'].config(text='VELOCITY:')
                labels['val_1']['value'].config(text=msg.bytes()[1])
                labels['val_2']['value'].config(text=msg.bytes()[2])
            case 'control_change':
                labels['val_1']['label'].config(text='CONTROL:')
                labels['val_2']['label'].config(text='VALUE:')
                labels['val_1']['value'].config(text=msg.bytes()[1])
                labels['val_2']['value'].config(text=msg.bytes()[2])
            case 'pitchwheel':
                labels['val_1']['label'].config(text='PITCH:')
                labels['val_2']['label'].config(text='')
                labels['val_1']['value'].config(text=msg.pitch)
                labels['val_2']['value'].config(text='')

    # PRIVATE #################################################################

    def _create_midi_bar(self, source):
        midi_bar = tk.Frame(self)
        main_label = tk.Label(midi_bar, text=f'{source.upper()}:')
        main_label.grid(row=0, column=0, padx=10)

        self.midi_labels[source] = {}

        for i, name in enumerate(['channel', 'type', 'val_1', 'val_2']):
            midi_bar.columnconfigure(i+1, weight=1, uniform='yiiiha')
            container = tk.Frame(midi_bar)
            self.midi_labels[source][name] = {
                'label': tk.Label(container),
                'value': tk.Label(container)
            }
            self.midi_labels[source][name]['label'].grid(row=0, column=0)
            self.midi_labels[source][name]['value'].grid(row=0, column=1)
            container.grid(row=0, column=i+1, sticky='ew')

        return midi_bar
