import tkinter.ttk as ttk


class RuleFormFrame(ttk.Frame):
    # INPUT VALUES ####################
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    def __init__(self, rule_form_view, source):
        super().__init__(rule_form_view)

        # CONTAINERS ##################
        self.frames = {}
        for i, key in enumerate(['title', 'ch', 'type', 'val1', 'val2']):
            self.frames[key] = ttk.Frame(self)

        # TITLE #######################
        if source == 'in':
            title = 'When MIDI IN is :'
        else:
            title = 'Route it TO :'
        title_label = ttk.Label(self.frames['title'], text=title,
                                style='bold.TLabel',
                                )
        title_label.grid(row=0, column=0, sticky='ew', pady=10)

        # CHANNEL INPUT ###############
        self._create_inputs_for(self.frames['ch'], 'CH', self.RANGE_16)

        # TYPE INPUT ##################
        type_inputs = self._create_inputs_for(self.frames['type'], 'TYPE',
                                              self.TYPES)
        # TYPE SELECTION EVENT ########
        type_inputs['input'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(
                event, type_inputs['input']))

        # LAYOUT ######################
        self.columnconfigure(0, weight=1)
        for i, frame in enumerate(self.frames.values()):
            # Title frame
            if i == 0:
                self.rowconfigure(i, weight=0)
                frame.grid(row=i)
                continue
            self.rowconfigure(i, weight=1, uniform='form')
            frame.grid(row=i, sticky='nsew')

    # INPUT BUILDING ##########################################################

    def _on_type_selected(self, event, type_input):
        self._clear_inputs()

        match type_input.get():
            case 'note_on' | 'note_off':
                self._create_note_inputs()
            case 'control_change':
                self._create_control_inputs()
            case 'pitchwheel':
                self._create_pitch_wheel_inputs()

    def _clear_inputs(self):
        val_1_inputs = self.frames['val1'].winfo_children()
        val_2_inputs = self.frames['val2'].winfo_children()
        for widget in [*val_1_inputs, *val_2_inputs]:
            widget.destroy()

    def _create_note_inputs(self):
        note_container = self.frames['val1']
        self._create_inputs_for(note_container,
                                'NOTE',
                                self.RANGE_128)
        velo_container = self.frames['val2']
        self._create_inputs_for(velo_container,
                                'VELOCITY',
                                self.RANGE_128)

    def _create_control_inputs(self):
        control_container = self.frames['val1']
        self._create_inputs_for(control_container,
                                'CONTROL',
                                self.RANGE_128)
        value_container = self.frames['val2']
        self._create_inputs_for(value_container,
                                'VALUE',
                                self.RANGE_128)

    def _create_pitch_wheel_inputs(self):
        pitch_container = self.frames['val1']
        self._create_inputs_for(pitch_container,
                                'PITCH',
                                self.RANGE_128)

    # INPUTS ##################################################################

    def _create_inputs_for(self, container, text, values):
        elements = {
            'label': ttk.Label(
                container, text=text,
                style='bold.TLabel',
                anchor='e',
                background='white'
            ),
            'input': ttk.Combobox(container, values=values,
                                  state='readonly',
                                  width=10),
        }
        # Set data for form handling
        match text:
            case 'CH':
                elements['label'].data = {'mido_name': 'channel'}
            case 'TYPE':
                elements['label'].data = {'mido_name': 'type'}
            case 'NOTE':
                elements['label'].data = {'mido_name': 'note'}
            case 'VELOCITY':
                elements['label'].data = {'mido_name': 'velocity'}
            case 'CONTROL':
                elements['label'].data = {'mido_name': 'control'}
            case 'VALUE':
                elements['label'].data = {'mido_name': 'value'}
            case 'PITCH':
                elements['label'].data = {'mido_name': 'pitch'}

        elements['input'].current(0)  # Set default value
        elements['label'].grid(row=0, column=0, sticky='ew')
        elements['input'].grid(row=0, column=1)

        container.rowconfigure(0, weight=1)
        # Label column ('CH', ...)
        container.columnconfigure(0, weight=0, minsize=80)
        # Inputs column (Comboboxes)
        container.columnconfigure(1, weight=3)

        return elements
