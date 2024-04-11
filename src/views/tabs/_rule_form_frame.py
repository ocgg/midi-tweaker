import tkinter.ttk as ttk


class RuleFormFrame(ttk.Frame):
    # INPUT VALUES ####################
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    def __init__(self, rule_form_view, source):
        super().__init__(rule_form_view)

        # FORM HANDLING ###############
        self.inputs = {}

        # CONTAINERS ##################
        inputs_names = ['ch', 'type', 'val1', 'val2']
        self.frames = {}
        containers = ['title'] + inputs_names + ['learn']
        for i, key in enumerate(containers):
            self.frames[key] = ttk.Frame(self)

        # TITLE #######################
        title = 'When MIDI IN is :' if source == 'in' else 'Route it TO :'

        self.frames['title'].rowconfigure(0, weight=1)
        self.frames['title'].columnconfigure(0, weight=1)
        title_label = ttk.Label(self.frames['title'], text=title,
                                anchor='center')
        title_label.config(style='bold.TLabel')
        title_label.grid(row=0, column=0, pady=10)

        # CHANNEL INPUT ###############
        self._create_inputs_for(self.frames['ch'], 'CH', self.RANGE_16)

        # TYPE INPUT ##################
        type_inputs = self._create_inputs_for(self.frames['type'], 'TYPE',
                                              self.TYPES)
        # Type selection event
        type_inputs['input'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(event, type_inputs['input'])
        )

        # LEARN BUTTON ################
        self.frames['learn'].rowconfigure(0, weight=1)
        self.frames['learn'].columnconfigure(0, weight=1)
        learn_btn = ttk.Button(self.frames['learn'], text='LEARN')
        learn_btn.config(style='learn.TButton')
        learn_btn.grid(row=0, column=0)
        self.learn_btn = learn_btn

        # LAYOUT ######################
        self.columnconfigure(0, weight=1)

        # Title frame
        self.rowconfigure(0, weight=0)
        self.frames['title'].grid(row=0, sticky='ew')

        # Inputs frames
        for i, frame in enumerate(self.frames.values()):
            self.rowconfigure(i+1, minsize=45)
            frame.grid(row=i+1, sticky='ew')

    # FORM HANDLING ###########################################################

    def get_form_state(self):
        input_values = {}

        for key, input in self.inputs.items():
            if not input or input.get() == self.ALL:
                continue
            value = input.get()
            value = int(value)-1 if value.isdigit() else value
            input_values[key] = value
        return input_values

    def set_form_state(self, midi_msg):
        self.inputs['channel'].current(midi_msg.channel+1)
        self.inputs['type'].set(midi_msg.type)
        self.inputs['type'].event_generate('<<ComboboxSelected>>')
        if midi_msg.type == 'note_on' or midi_msg.type == 'note_off':
            self.inputs['note'].set(midi_msg.note-1)
            self.inputs['velocity'].set(midi_msg.velocity+1)
        elif midi_msg.type == 'control_change':
            self.inputs['control'].set(midi_msg.control+1)
            self.inputs['value'].set(midi_msg.value+1)
        elif midi_msg.type == 'pitchwheel':
            self.inputs['pitch'].set(midi_msg.pitch+1)

    def _update_inputs(self, elements, text):
        # Called by _create_inputs_for(), triggered by _on_type_selected()
        # self.inputs keys must match a mido msg property
        # case values must match the input's Label text
        match text:
            case 'CH':
                self.inputs['channel'] = elements['input']
            case 'TYPE':
                self.inputs['type'] = elements['input']
            case 'NOTE':
                self.inputs['note'] = elements['input']
            case 'VELOCITY':
                self.inputs['velocity'] = elements['input']
            case 'CONTROL':
                self.inputs['control'] = elements['input']
            case 'VALUE':
                self.inputs['value'] = elements['input']
            case 'PITCH':
                self.inputs['pitch'] = elements['input']

    # TYPE SELECTION EVENT ####################################################

    def _on_type_selected(self, event, type_input):
        self._clear_inputs()

        val1_frame = self.frames['val1']
        val2_frame = self.frames['val2']

        match type_input.get():
            case 'note_on' | 'note_off':
                self._create_inputs_for(val1_frame, 'NOTE', self.RANGE_128)
                self._create_inputs_for(val2_frame, 'VELOCITY', self.RANGE_128)
            case 'control_change':
                self._create_inputs_for(val1_frame, 'CONTROL', self.RANGE_128)
                self._create_inputs_for(val2_frame, 'VALUE', self.RANGE_128)
            case 'pitchwheel':
                self._create_inputs_for(val1_frame, 'PITCH', self.RANGE_128)

    def _clear_inputs(self):
        val1_widgets = self.frames['val1'].winfo_children()
        val2_widgets = self.frames['val2'].winfo_children()
        for widget in [*val1_widgets, *val2_widgets]:
            widget.destroy()

        inputs = self.inputs.items()
        to_keep = ['channel', 'type']
        self.inputs = {k: v for k, v in inputs if k in to_keep}

    # INPUTS BUILDING #########################################################

    def _create_inputs_for(self, container, text, values):
        # Widgets init
        elements = {
            'label': ttk.Label(
                container, text=text,
                style='bold.gray.TLabel',
            ),
            'input': ttk.Combobox(container, values=values,
                                  state='readonly',
                                  width=15),
        }
        # Widget layout in container
        elements['input'].current(0)  # Set default value
        elements['label'].grid(row=0, column=0, sticky='e')
        elements['input'].grid(row=0, column=1, sticky='w', padx=(10, 0))

        # Container layout
        container.rowconfigure(0, weight=1)
        # Label column ('CH', 'TYPE', ...)
        container.columnconfigure(0, weight=1, minsize=80)
        # Inputs column (Comboboxes)
        container.columnconfigure(1, weight=1, minsize=210)

        # Update inputs for form handling
        self._update_inputs(elements, text)

        return elements

    # LEARN BTN STUFF #########################################################

    def set_learn_btn_active(self):
        self.learn_btn.config(text='Stop', style='learning.TButton')

    def set_learn_btn_normal(self):
        self.learn_btn.config(text='Learn', style='learn.TButton')
