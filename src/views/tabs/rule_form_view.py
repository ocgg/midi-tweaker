import tkinter.ttk as ttk


class RuleFormView(ttk.Frame):

    # INPUT VALUES ####################
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    def __init__(self, master):
        super().__init__(master)

        self.form_frames = {'in': {}, 'out': {}}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # IN FORM #####################

        in_form_frame = self._build_form_frame(self)

        # SEPARATOR ###################

        separator = ttk.Frame(self)
        separator.rowconfigure(0, weight=1)
        separator.rowconfigure(2, weight=1)

        sep_1 = ttk.Separator(separator, orient='vertical')
        sep_label = ttk.Label(separator, text='⮕')
        sep_2 = ttk.Separator(separator, orient='vertical')

        sep_1.grid(row=0, column=0, sticky='ns')
        sep_label.grid(row=1, column=0)
        sep_2.grid(row=2, column=0, sticky='ns')

        # OUT FORM ####################

        out_form_frame = self._build_form_frame(self, source='out')

        # SUBMIT BUTTON ###############

        self.submit_btn = ttk.Button(self, text='Done', style='big.TButton')
        self.submit_btn.grid(row=1, column=0, columnspan=3, pady=10)

        # LAYOUT ######################

        in_form_frame.grid(row=0, column=0, sticky='nsew')
        separator.grid(row=0, column=1, sticky='ns')
        out_form_frame.grid(row=0, column=2, sticky='nsew')

    # LAYOUT ##################################################################

    def _build_form_frame(self, frame, source='in'):
        form_frame = ttk.Frame(self)

        form_frames = self.form_frames[source]

        title = 'When MIDI IN is :' if source == 'in' else 'Route it to :'
        form_title = ttk.Label(form_frame, text=title)
        form_frames['ch'] = ttk.Frame(form_frame)
        form_frames['type'] = ttk.Frame(form_frame)
        form_frames['val1'] = ttk.Frame(form_frame)
        form_frames['val2'] = ttk.Frame(form_frame)

        # Channel input ###############
        ch_inputs = self._ch_inputs(form_frames['ch'])
        ch_inputs['label'].grid(row=0, column=0)
        ch_inputs['input'].grid(row=0, column=1)

        # Type input ##################
        type_inputs = self._type_inputs(form_frames['type'])
        type_inputs['label'].grid(row=0, column=0)
        type_inputs['input'].grid(row=0, column=1)

        # Layout ######################
        form_title.grid(row=0, column=0)
        form_frames['ch'].grid(row=1, column=0)
        form_frames['type'].grid(row=2, column=0)
        form_frames['val1'].grid(row=3, column=0)
        form_frames['val2'].grid(row=4, column=0)

        # Events ######################
        type_inputs['input'].bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(
                event, source, type_inputs['input']))

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
        note_inputs = self._note_inputs(note_container)
        note_inputs['label'].grid(row=0, column=0)
        note_inputs['input'].grid(row=0, column=1)

        velo_container = self.form_frames[source]['val2']
        velo_inputs = self._velocity_inputs(velo_container)
        velo_inputs['label'].grid(row=0, column=0)
        velo_inputs['input'].grid(row=0, column=1)

    def _create_control_inputs(self, source):
        control_container = self.form_frames[source]['val1']
        control_inputs = self._control_inputs(control_container)
        control_inputs['label'].grid(row=0, column=0)
        control_inputs['input'].grid(row=0, column=1)

        value_container = self.form_frames[source]['val2']
        value_inputs = self._value_inputs(value_container)
        value_inputs['label'].grid(row=0, column=0)
        value_inputs['input'].grid(row=0, column=1)

    def _create_pitch_wheel_inputs(self, source):
        pitch_container = self.form_frames[source]['val1']
        pitch_inputs = self._pitch_wheel_inputs(pitch_container)
        pitch_inputs['label'].grid(row=0, column=0)
        pitch_inputs['input'].grid(row=0, column=1)

    # INPUTS ##################################################################

    def _pitch_wheel_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='PITCH:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_128,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'pitch'}
        elements['input'].current(0)
        return elements

    def _value_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='VALUE:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_128,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'value'}
        elements['input'].current(0)
        return elements

    def _control_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='CONTROL:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_128,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'control'}
        elements['input'].current(0)
        return elements

    def _velocity_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='VELOCITY:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_128,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'velocity'}
        elements['input'].current(0)
        return elements

    def _note_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='NOTE:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_128,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'note'}
        elements['input'].current(0)
        return elements

    def _type_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='TYPE:'),
                    'input': ttk.Combobox(frame,
                                          values=self.TYPES,
                                          state='readonly',
                                          width=17),
                    }
        elements['label'].data = {'mido_name': 'type'}
        elements['input'].current(0)
        return elements

    def _ch_inputs(self, frame):
        elements = {'label': ttk.Label(frame, text='CH:'),
                    'input': ttk.Combobox(frame,
                                          values=self.RANGE_16,
                                          state='readonly',
                                          width=4),
                    }
        elements['label'].data = {'mido_name': 'channel'}
        elements['input'].current(0)  # Default value to 'all'

        return elements
