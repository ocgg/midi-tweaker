import tkinter as tk
import tkinter.ttk as ttk
from .rules_list_view import RulesListView
from .rule_form_view import RuleFormView
from src.modules.constants import (
    PORT_CHOICE_NONE,
    PORT_CHOICE_ALL,
    PORT_CHOICE_PLACEHOLDER,
    PORT_CHOICE_NEW,
)


class TabView(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(main_frame)
        self.main_frame = main_frame

        self.frames = {}
        self.midi_bars = {'in': {}, 'out': {}}

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # MIDI IN bar
        midi_in_bar = self._create_midi_bar('in')
        # MAIN CONTENT:
        self.frames['form'] = RuleFormView(self)
        self.frames['list'] = RulesListView(self)
        # MIDI OUT bar
        midi_out_bar = self._create_midi_bar('out')

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
        labels = self.midi_bars[source]
        msg_type = msg.type.replace('_', ' ')
        labels['type']['label'].config(text='TYPE')
        labels['type']['value'].config(text=msg_type)
        labels['channel']['label'].config(text='CH')
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

    def update_midi_ports(self, source, ports):
        combobox = self.midi_bars[source]['ports']['combobox']
        combobox['values'] = (PORT_CHOICE_NONE,)
        if source == 'in':
            combobox['values'] += (PORT_CHOICE_ALL,)
        combobox['values'] += tuple(ports)
        if source == 'out':
            combobox['values'] += (PORT_CHOICE_NEW,)
        combobox.set(PORT_CHOICE_PLACEHOLDER)

    def ask_new_port_name(self):
        self.new_port_toplevel = tk.Toplevel(self)
        self.new_port_toplevel.title('New Virtual Out MIDI Port')
        self.new_port_toplevel.resizable(False, False)
        # Keep the Toplevel on top of the main window
        self.new_port_toplevel.transient(self.main_frame)
        # Deactivate the main window while Toplevel is open
        self.new_port_toplevel.grab_set()

        toplevel_width = self.new_port_toplevel.winfo_reqwidth()
        toplevel_height = self.new_port_toplevel.winfo_reqheight()
        root_width = self.winfo_width()
        root_height = self.winfo_height()

        x = int(root_width / 2)
        y = int(root_height / 2)
        middle = f"{toplevel_width}x{toplevel_height}+{x}+{y}"

        self.new_port_toplevel.geometry(middle)

        text = 'Enter the new port name:'
        label = ttk.Label(self.new_port_toplevel, text=text)
        self.new_port_entry = ttk.Entry(self.new_port_toplevel)
        self.create_port_btn = ttk.Button(self.new_port_toplevel, text='Create',
                                          style='TButton')

        label.grid(row=0, column=0, columnspan=2, sticky='ew', pady=5)
        self.new_port_entry.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)
        self.create_port_btn.grid(row=2, column=0, columnspan=2, pady=5)

    # PRIVATE #################################################################

    def _create_midi_bar(self, source):
        midi_bar_frame = ttk.Frame(self)
        midi_bar_frame.rowconfigure(0, weight=1)
        midi_bar_frame.columnconfigure(0, minsize=55)   # 'IN'/'OUT' label
        midi_bar_frame.columnconfigure(1, minsize=100)  # Port choice container
        midi_bar_frame.columnconfigure(2, minsize=50)   # Channel
        midi_bar_frame.columnconfigure(3, minsize=150)  # Type
        midi_bar_frame.columnconfigure(4, minsize=100)  # Value 1
        midi_bar_frame.columnconfigure(5, minsize=100)  # Value 2

        midi_bar_data = self.midi_bars[source]

        # 'IN' or 'OUT' label
        main_label = ttk.Label(midi_bar_frame, text=source.upper(),
                               style='big.TLabel', anchor='center')

        # Port choice
        port_choice_container = ttk.Frame(midi_bar_frame)
        port_choice = ttk.Combobox(port_choice_container, state='readonly')
        refresh_btn = ttk.Button(port_choice_container, text='↺',
                                 style='icon.TButton')
        midi_bar_data['ports'] = {
            'combobox': port_choice,
            'refresh': refresh_btn
        }
        port_choice.grid(row=0, column=0, sticky='ew')
        refresh_btn.grid(row=0, column=1)

        # Labels for message data
        MIDI_DATA = ['channel', 'type', 'val_1', 'val_2']

        for i, name in enumerate(MIDI_DATA):
            container = ttk.Frame(midi_bar_frame)
            container.rowconfigure(0, weight=1)
            container.columnconfigure(1, weight=1)

            midi_bar_data[name] = {
                'container': container,
                'label': ttk.Label(container, style='bold.TLabel'),
                'value': ttk.Label(container, style='bold.gray.TLabel')
            }
            midi_bar_data[name]['label'].grid(row=0, column=0,
                                              sticky='w', padx=(0, 3))
            midi_bar_data[name]['value'].grid(row=0, column=1,
                                              sticky='w')

        # Layout for midi_bar_frame content
        main_label.grid(row=0, column=0, sticky='ew', pady=3)
        port_choice_container.grid(row=0, column=1, sticky='ew', padx=(0, 5))
        for i, name in enumerate(MIDI_DATA):
            container = midi_bar_data[name]['container']
            container.grid(row=0, column=i+2, sticky='ew')

        return midi_bar_frame
