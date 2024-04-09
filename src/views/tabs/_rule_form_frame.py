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

        # LAYOUT ######################
        self.columnconfigure(0, weight=1)

        # Title frame
        self.rowconfigure(0, weight=0)
        self.frames['title'].grid(row=0, sticky='ew')

        # Inputs frames
        for i, frame in enumerate(self.frames.values()):
            # self.rowconfigure(i+1, uniform='form', weight=1)
            frame.grid(row=i+1, sticky='ew', pady=(0, 10))

    # INPUT BUILDING ##########################################################

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
        val_1_inputs = self.frames['val1'].winfo_children()
        val_2_inputs = self.frames['val2'].winfo_children()
        for widget in [*val_1_inputs, *val_2_inputs]:
            widget.destroy()

    # INPUTS ##################################################################

    def _create_inputs_for(self, container, text, values):
        elements = {
            'label': ttk.Label(
                container, text=text,
                style='bold.TLabel',
            ),
            'input': ttk.Combobox(container, values=values,
                                  state='readonly',
                                  width=15),
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
        elements['label'].grid(row=0, column=0, sticky='e')
        elements['input'].grid(row=0, column=1, sticky='w', padx=(10, 0))

        container.rowconfigure(0, weight=1)
        # Label column ('CH', ...)
        container.columnconfigure(0, weight=1, minsize=80)
        # Inputs column (Comboboxes)
        container.columnconfigure(1, weight=1, minsize=210)

        return elements
