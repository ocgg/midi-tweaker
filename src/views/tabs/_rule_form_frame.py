import tkinter.ttk as ttk


class RuleFormFrame(ttk.Frame):
    # INPUT VALUES ####################
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    def __init__(self, rule_form_view, source):
        super().__init__(rule_form_view)

        self.form_frames = {'in': {}, 'out': {}}

        # MAIN CONTAINER ##############
        self.columnconfigure(0, weight=1)
        for i in range(5):
            self.rowconfigure(i, weight=1, uniform='form')

        # CONTAINERS ##################
        form_frames = self.form_frames[source]

        for i, key in enumerate(['title', 'ch', 'type', 'val1', 'val2']):
            form_frames[key] = ttk.Frame(self)

        # CONTAINER'S FRAMES ##########
        # Title
        title = 'When MIDI IN is :' if source == 'in' else 'Route it to :'
        title_label = ttk.Label(form_frames['title'], text=title,
                                style='bold.TLabel')
        title_label.grid(row=0, column=0, columnspan=2)
        # Channel input
        self._create_inputs_for(form_frames['ch'], 'CH', self.RANGE_16)
        # Type input
        type_inputs = self._create_inputs_for(form_frames['type'], 'TYPE',
                                              self.TYPES)
        # Event on type selection
        type_inputs['input'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(
                event, source, type_inputs['input']))

        # LAYOUT ######################
        for i, frame in enumerate(form_frames.values()):
            frame.grid(row=i, column=0, sticky='nsew')

    # LAYOUT ##################################################################

    def _build_form_frame(self, source='in'):
        # MAIN CONTAINER ##############
        form_frame = ttk.Frame(self)
        form_frame.columnconfigure(0, weight=1)
        for i in range(5):
            form_frame.rowconfigure(i, weight=1, uniform='form')

        # CONTAINERS ##################
        form_frames = self.form_frames[source]

        for i, key in enumerate(['title', 'ch', 'type', 'val1', 'val2']):
            form_frames[key] = ttk.Frame(form_frame)

        # CONTAINER'S FRAMES ##########
        # Title
        title = 'When MIDI IN is :' if source == 'in' else 'Route it to :'
        title_label = ttk.Label(form_frames['title'], text=title,
                                style='bold.TLabel')
        title_label.grid(row=0, column=0, columnspan=2)
        # Channel input
        self._create_inputs_for(form_frames['ch'], 'CH', self.RANGE_16)
        # Type input
        type_inputs = self._create_inputs_for(form_frames['type'], 'TYPE',
                                              self.TYPES)
        # Event on type selection
        type_inputs['input'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(
                event, source, type_inputs['input']))

        # LAYOUT ######################
        for i, frame in enumerate(form_frames.values()):
            frame.grid(row=i, column=0, sticky='nsew')

        return form_frame

    # INPUT BUILDING ##########################################################

    def _on_type_selected(self, event, source, type_input):
        self._clear_inputs(source)

        match type_input.get():
            case 'note_on':
                self._create_note_inputs(source)
            case 'note_off':
                self._create_note_inputs(source)
            case 'control_change':
                self._create_control_inputs(source)
            case 'pitchwheel':
                self._create_pitch_wheel_inputs(source)

    def _clear_inputs(self, source):
        val_1_inputs = self.form_frames[source]['val1'].winfo_children()
        val_2_inputs = self.form_frames[source]['val2'].winfo_children()
        for widget in [*val_1_inputs, *val_2_inputs]:
            widget.destroy()

    def _create_note_inputs(self, source):
        note_container = self.form_frames[source]['val1']
        self._create_inputs_for(note_container,
                                'NOTE',
                                self.RANGE_128)
        velo_container = self.form_frames[source]['val2']
        self._create_inputs_for(velo_container,
                                'VELOCITY',
                                self.RANGE_128)

    def _create_control_inputs(self, source):
        control_container = self.form_frames[source]['val1']
        self._create_inputs_for(control_container,
                                'CONTROL',
                                self.RANGE_128)
        value_container = self.form_frames[source]['val2']
        self._create_inputs_for(value_container,
                                'VALUE',
                                self.RANGE_128)

    def _create_pitch_wheel_inputs(self, source):
        pitch_container = self.form_frames[source]['val1']
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
