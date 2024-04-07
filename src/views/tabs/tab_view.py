import tkinter.ttk as ttk
from .rules_list_view import RulesListView
from .rule_form_view import RuleFormView


class TabView(ttk.Frame):
    # STYLES ##########
    norm = {'font': ('sans-serif', 11)}
    bold = {'font': ('sans-serif', 11, 'bold')}
    big_bold = {'font': ('sans-serif', 14, 'bold')}

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
        self.midi_labels['in']['channel']['label'].config(text='CH')
        self.midi_labels['in']['type']['label'].config(text='TYPE')
        self.midi_labels['out']['channel']['label'].config(text='CH')
        self.midi_labels['out']['type']['label'].config(text='TYPE')

        # LAYOUT
        midi_in_bar.grid(row=0, sticky='ew')
        ttk.Separator(self, orient='horizontal').grid(row=1, sticky='ew')
        self.frames['form'].grid(row=2, sticky="nsew")
        self.frames['list'].grid(row=2, sticky="nsew")
        ttk.Separator(self, orient='horizontal').grid(row=3, sticky='ew')
        midi_out_bar.grid(row=4, sticky='nsew')

    # DISPLAYING ##############################################################

    def display_rule_form(self):
        self.frames['form'].lift()

    def display_rules_list(self):
        self.frames['list'].lift()

    def display_midi_msg(self, source, msg):
        labels = self.midi_labels[source]
        msg_type = msg.type.replace('_', ' ')
        labels['type']['value'].config(text=msg_type)
        labels['channel']['value'].config(text=msg.channel)
        match msg.type:
            case 'note_on' | 'note_off':
                labels['val_1']['label'].config(text='NOTE')
                labels['val_1']['value'].config(text=msg.bytes()[1])
                labels['val_2']['label'].config(text='VELOCITY')
                labels['val_2']['value'].config(text=msg.bytes()[2])
            case 'control_change':
                labels['val_1']['label'].config(text='CONTROL')
                labels['val_1']['value'].config(text=msg.bytes()[1])
                labels['val_2']['label'].config(text='VALUE')
                labels['val_2']['value'].config(text=msg.bytes()[2])
            case 'pitchwheel':
                labels['val_1']['label'].config(text='PITCH')
                labels['val_1']['value'].config(text=msg.pitch)
                labels['val_2']['label'].config(text='')
                labels['val_2']['value'].config(text='')

    # PRIVATE #################################################################

    def _create_midi_bar(self, source):
        midi_bar = ttk.Frame(self)
        midi_bar.rowconfigure(0, weight=1)
        midi_bar.columnconfigure(0, minsize=60)
        midi_bar.columnconfigure(0, minsize=50,  weight=2, uniform='a')
        midi_bar.columnconfigure(1, minsize=50,  weight=3, uniform='a')
        midi_bar.columnconfigure(2, minsize=180, weight=5, uniform='a')
        midi_bar.columnconfigure(3, minsize=100, weight=4, uniform='a')
        midi_bar.columnconfigure(4, minsize=100, weight=4, uniform='a')

        main_label = ttk.Label(midi_bar, text=source.upper(), **self.big_bold)
        main_label.grid(row=0, column=0, sticky='w', padx=7, pady=3)

        self.midi_labels[source] = {}

        for i, name in enumerate(['channel', 'type', 'val_1', 'val_2']):
            container = ttk.Frame(midi_bar)
            container.rowconfigure(0, weight=1)
            self.midi_labels[source][name] = {
                'label': ttk.Label(container, **self.bold, foreground='gray'),
                'value': ttk.Label(container, **self.bold)
            }
            self.midi_labels[source][name]['label'].grid(row=0, column=0,
                                                         sticky='nse', padx=5)
            self.midi_labels[source][name]['value'].grid(row=0, column=1,
                                                         sticky='nsw')
            container.grid(row=0, column=i+1, sticky='nsew')

        return midi_bar
