import tkinter.ttk as ttk
from src.modules.constants import (
        MIDO_TYPE_TO_VAL1,
        MIDO_TYPE_TO_VAL2,
        MIDO_TYPE_TO_VALUES,
)


class RuleFormFrame(ttk.Frame):
    # INPUT VALUES ####################
    DEFAULT_VALUE = ''
    TYPES = [DEFAULT_VALUE,
             'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [DEFAULT_VALUE] + [i for i in range(1, 17)]
    RANGE_128 = [DEFAULT_VALUE] + [i for i in range(1, 129)]

    def __init__(self, rule_form_view, source):
        super().__init__(rule_form_view)

        self.inputs = {}
        self.labels = {}

        # WIDGETS #########################################

        # TITLE #######################
        title_txt = 'When MIDI IN is :' if source == 'in' else 'Route it TO :'
        title_label = ttk.Label(self, text=title_txt, anchor='center')
        title_label.config(style='bold.TLabel')

        # CHANNEL INPUT ###############
        channel_label = ttk.Label(self, text='CH', style='bold.gray.TLabel')
        channel_input = ttk.Combobox(self, values=self.RANGE_16, width=15)
        self.labels['channel'] = channel_label
        self.inputs['channel'] = channel_input

        # TYPE INPUT ##################
        type_label = ttk.Label(self, text='TYPE', style='bold.gray.TLabel')
        type_input = ttk.Combobox(self, values=self.TYPES, width=15)
        self.labels['type'] = type_label
        self.inputs['type'] = type_input

        # VAL 1 INPUT #################
        val1_label = ttk.Label(self, text='VALUE 1', style='bold.gray.TLabel')
        val1_input = ttk.Combobox(self, values=self.RANGE_128, width=15)
        self.labels['val1'] = val1_label
        self.inputs['val1'] = val1_input

        # VAL 2 INPUT #################
        val2_label = ttk.Label(self, text='VALUE 2', style='bold.gray.TLabel')
        val2_input = ttk.Combobox(self, values=self.RANGE_128, width=15)
        self.labels['val2'] = val2_label
        self.inputs['val2'] = val2_input

        # LEARN BUTTON ################
        self.learn_btn = ttk.Button(self, text='Learn')
        self.learn_btn.config(style='learn.TButton')

        # LAYOUT ##########################################

        # Title
        self.rowconfigure(0, weight=0)
        title_label.grid(row=0, columnspan=2, sticky='ew', pady=20)

        # Inputs
        PADX = {'padx': (0, 10)}
        PADY = {'pady': (0, 30)}

        self.columnconfigure(0, weight=0, minsize=100)
        for i, label in enumerate(self.labels.values(), start=1):
            label.grid(row=i, column=0, sticky='e', **PADY, **PADX)

        self.columnconfigure(1, weight=2)
        for i, input in enumerate(self.inputs.values(), start=1):
            input.grid(row=i, column=1, sticky='ew', **PADY, padx=(0, 20))

        # Learn button
        self.rowconfigure(5, weight=1)
        self.learn_btn.grid(row=len(self.labels)+1, column=0, columnspan=2)

        # INPUTS INIT #####################################

        # TYPE SELECTION EVENT ########
        self.inputs['type'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(event)
        )
        # DEFAULTS VALUES & STATES ####
        self.inputs['channel'].current(0)
        self.inputs['type'].current(0)

        self.inputs['type'].config(state='readonly')
        self.inputs['val1'].config(state='disabled')
        self.inputs['val2'].config(state='disabled')

        # ALIASES #########################################
        # These are for easier management of values 1 & 2 names

        for name in MIDO_TYPE_TO_VAL1.values():
            self.inputs[name] = self.inputs['val1']
            self.labels[name] = self.labels['val1']

        for name in MIDO_TYPE_TO_VAL2.values():
            self.inputs[name] = self.inputs['val2']
            self.labels[name] = self.labels['val2']

    # INPUTS PROPERTY #########################################################

    @property
    def form_data(self):
        # Called by tab_controller for form handling
        # Filters self.inputs aliases to get right val1 & val2 keys names
        # Filters empty values
        form_data = {}
        form_data['channel'] = self.inputs['channel'].get().replace(' ', '')
        # Don't remove spaces here since type field is read-only
        form_data['type'] = self.inputs['type'].get()
        selected_type = form_data['type']
        if selected_type:
            for name in MIDO_TYPE_TO_VALUES[selected_type]:
                form_data[name] = self.inputs[name].get().replace(' ', '')
        # Return non-empty values
        return {k: v for k, v in form_data.items() if v}

    # TYPE SELECTION EVENT ####################################################

    def _on_type_selected(self, event):
        selected_type = event.widget.get()

        val1_name = MIDO_TYPE_TO_VAL1.get(selected_type)
        if val1_name:
            self.labels[val1_name].config(text=val1_name.upper())
            self.inputs[val1_name].config(state='normal')
        else:
            self.labels['val1'].config(text='VALUE 1')
            self.inputs['val1'].config(state='disabled')

        val2_name = MIDO_TYPE_TO_VAL2.get(selected_type)
        if val2_name:
            self.labels[val2_name].config(text=val2_name.upper())
            self.inputs[val2_name].config(state='normal')
        else:
            self.labels['val2'].config(text='VALUE 2')
            self.inputs['val2'].config(state='disabled')

    # LEARN ###################################################################

    def set_learn_btn_active(self):
        self.learn_btn.config(text='Stop', style='learning.TButton')

    def set_learn_btn_normal(self):
        self.learn_btn.config(text='Learn', style='learn.TButton')

    def set_form_state(self, midi_msg):
        self.inputs['channel'].set(midi_msg.channel)
        self.inputs['type'].set(midi_msg.type)
        self.inputs['type'].event_generate('<<ComboboxSelected>>')

        # TODO: verify if it works thanks to aliases:
        for k, v in midi_msg.dict().items():
            if self.inputs.get(k):
                self.inputs[k].set(v)

    # VALIDATIONS #############################################################

    def display_errors(self, form_data):
        # TODO:
        print(form_data)
