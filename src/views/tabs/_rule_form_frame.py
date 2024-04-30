import tkinter.ttk as ttk
from src.modules.constants import (
        MIDO_TYPE_TO_VAL1,
        MIDO_TYPE_TO_VAL2,
        MIDO_TYPE_TO_VALUES,
        FORM_ATTR_RANGE,
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
        self.field_error_labels = {}

        # WIDGETS #########################################

        # TITLE #######################
        title_txt = 'When MIDI IN is :' if source == 'in' else 'Route it TO :'
        title_label = ttk.Label(self, text=title_txt, anchor='center')
        title_label.config(style='bold.TLabel')

        # GLOBAL ERROR LABEL #########
        self.global_error_label = ttk.Label(self, style='error.TLabel',
                                            anchor='center')

        # CHANNEL INPUT ###############
        channel_label = ttk.Label(self, text='CH', style='bold.gray.TLabel')
        channel_input = ttk.Combobox(self, values=self.RANGE_16, width=15)
        channel_valid_lbl = ttk.Label(self, style='error.TLabel')
        self.labels['channel'] = channel_label
        self.inputs['channel'] = channel_input
        self.field_error_labels['channel'] = channel_valid_lbl

        # TYPE INPUT ##################
        type_label = ttk.Label(self, text='TYPE', style='bold.gray.TLabel')
        type_input = ttk.Combobox(self, values=self.TYPES, width=15)
        type_valid_lbl = ttk.Label(self, style='error.TLabel')
        self.labels['type'] = type_label
        self.inputs['type'] = type_input
        self.field_error_labels['type'] = type_valid_lbl

        # VAL 1 INPUT #################
        val1_label = ttk.Label(self, text='VALUE 1', style='bold.gray.TLabel')
        val1_input = ttk.Combobox(self, values=self.RANGE_128, width=15)
        val1_valid_lbl = ttk.Label(self, style='error.TLabel')
        self.labels['val1'] = val1_label
        self.inputs['val1'] = val1_input
        self.field_error_labels['val1'] = val1_valid_lbl

        # VAL 2 INPUT #################
        val2_label = ttk.Label(self, text='VALUE 2', style='bold.gray.TLabel')
        val2_input = ttk.Combobox(self, values=self.RANGE_128, width=15)
        val2_valid_lbl = ttk.Label(self, style='error.TLabel')
        self.labels['val2'] = val2_label
        self.inputs['val2'] = val2_input
        self.field_error_labels['val2'] = val2_valid_lbl

        # LEARN BUTTON ################
        self.learn_btn = ttk.Button(self, text='Learn')
        self.learn_btn.config(style='learn.TButton')

        # LAYOUT ##########################################

        # TITLE (ROW 0) ###############
        title_label.grid(row=0, columnspan=2, pady=(20, 0))

        # GLOBAL ERROR LABEL (ROW 1) ##
        self.global_error_label.grid(row=1, columnspan=2, pady=(0, 20))

        # INPUTS (FROM ROW 2) #########
        PADX = {'padx': (0, 10)}
        PADY = {'pady': (5, 15)}

        # Labels, column 0
        self.columnconfigure(0, weight=0, minsize=100)
        for i, label in enumerate(self.labels.values(), start=1):
            label.grid(row=i*2, column=0, sticky='e', **PADX)

        # Inputs, column 1
        self.columnconfigure(1, weight=2)
        for i, input in enumerate(self.inputs.values(), start=1):
            input.grid(row=i*2, column=1, sticky='ew', padx=(0, 20))

        # Validation labels, inter-row
        for i, label in enumerate(self.field_error_labels.values(), start=1):
            label.grid(row=i*2+1, column=1, sticky='ew', **PADY)

        # Learn button
        self.rowconfigure(10, weight=1)
        self.learn_btn.grid(row=len(self.labels)*2+2, column=0, columnspan=2)

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
            self.field_error_labels[name] = self.field_error_labels['val1']

        for name in MIDO_TYPE_TO_VAL2.values():
            self.inputs[name] = self.inputs['val2']
            self.labels[name] = self.labels['val2']
            self.field_error_labels[name] = self.field_error_labels['val2']

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

        for k, v in midi_msg.dict().items():
            if self.inputs.get(k):
                self.inputs[k].set(v)

    # VALIDATIONS ERRORS ######################################################

    def display_field_errors(self, form_data):
        for field, input in form_data.items():
            if input or field == 'type':
                continue
            validation_label = self.field_error_labels[field]
            min = FORM_ATTR_RANGE[field][0]
            max = FORM_ATTR_RANGE[field][-1]
            error_msg = f'Should be a number or range between {min} and {max}.'
            validation_label.config(text=error_msg)

    def display_global_error(self):
        error_msg = 'Routed message should be different than the input.'
        self.global_error_label.config(text=error_msg)

    # CLEAR ###################################################################

    def clear_errors(self):
        for label in self.field_error_labels.values():
            label.config(text='')
        self.global_error_label.config(text='')

    def clear_form(self):
        for input in self.inputs.values():
            input.set('')
        self.inputs['type'].event_generate('<<ComboboxSelected>>')
