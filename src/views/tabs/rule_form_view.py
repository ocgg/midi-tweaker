import tkinter.ttk as ttk


class RuleFormView(ttk.Frame):
    # INPUT VALUES ##########
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    # STYLES ###############

    def __init__(self, master):
        super().__init__(master)
        self.TAB = master

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # IN FORM #############################################################

        in_form_frame = self._build_form(self)

        # SEPARATOR ###########################################################

        separator = ttk.Frame(self)
        separator.rowconfigure(0, weight=1)
        separator.rowconfigure(2, weight=1)

        ttk.Separator(separator, orient='vertical').grid(row=0, column=0, sticky='ns')
        ttk.Label(separator, text='⮕').grid(row=1, column=0)
        ttk.Separator(separator, orient='vertical').grid(row=2, column=0, sticky='ns')

        # OUT FORM ############################################################

        out_form_frame = self._build_form(self, source='out')

        # SUBMIT BUTTON #######################################################

        self.submit_btn = ttk.Button(self, text='Done', style='big.TButton')
        self.submit_btn.grid(row=1, column=0, columnspan=3, pady=10)

        # LAYOUT ##############################################################

        in_form_frame.grid(row=0, column=0, sticky='nsew')
        separator.grid(row=0, column=1, sticky='ns')
        out_form_frame.grid(row=0, column=2, sticky='nsew')

        # in_msg_form = self._build_form(in_msg_frame)
        # in_msg_frame.pack(side='top')
        #
        # ttk.Label(self, text='To:').pack(side='top')
        # out_msg_form = self._build_form(out_msg_frame)
        # out_msg_frame.pack(side='top')
        #

    # LAYOUT ##################################################################

    def _build_form(self, frame, source='in'):
        form_frame = ttk.Frame(self)
        # form_frame.rowconfigure(0, weight=1)
        # form_frame.columnconfigure(0, weight=1, uniform='col')
        # form_frame.columnconfigure(2, weight=1, uniform='col')

        title = 'When MIDI IN is :' if source == 'in' else 'Route it to :'
        form_title = ttk.Label(form_frame, text=title)
        ch_frame = ttk.Frame(form_frame)
        type_frame = ttk.Frame(form_frame)
        val_1_frame = ttk.Frame(form_frame)
        val_2_frame = ttk.Frame(form_frame)

        # Channel input ################
        ch_inputs = self._ch_inputs(ch_frame)
        ch_inputs['label'].grid(row=0, column=0)
        ch_inputs['input'].grid(row=0, column=1)

        # Type input ###################
        type_inputs = self._type_inputs(type_frame)
        type_inputs['label'].grid(row=0, column=0)
        type_inputs['input'].grid(row=0, column=1)

        # Layout #######################
        form_title.grid(row=0, column=0)
        ch_frame.grid(row=1, column=0)
        type_frame.grid(row=2, column=0)
        val_1_frame.grid(row=3, column=0)
        val_2_frame.grid(row=4, column=0)

        return form_frame

    # def _build_form(self, frame):
    #     inputs = self._base_inputs(frame)
    #
    #     inputs['ch']['label'].grid(row=0, column=0)
    #     inputs['ch']['input'].grid(row=0, column=1)
    #
    #     inputs['type']['label'].grid(row=0, column=2)
    #     msg_type = inputs['type']['input']
    #     msg_type.grid(row=0, column=3)
    #     msg_type.bind(
    #         '<<ComboboxSelected>>',
    #         lambda event: self._on_type_selected(event, frame, msg_type))

    # INPUT BUILDING ##########################################################

    def _on_type_selected(self, event, frame, type_input):
        self._clear_inputs(frame)

        match type_input.get():
            case 'note_on':
                self._create_note_inputs(frame)
            case 'note_off':
                self._create_note_inputs(frame)
            case 'control_change':
                self._create_control_inputs(frame)
            case 'pitchwheel':
                self._create_pitch_wheel_inputs(frame)

    def _clear_inputs(self, frame):
        for i, widget in enumerate(frame.winfo_children()):
            if i > 3:
                widget.destroy()

    def _create_note_inputs(self, frame):
        inputs = self._note_inputs(frame)
        inputs['note']['label'].grid(row=1, column=0)
        self.in_note = inputs['note']['input']
        self.in_note.grid(row=1, column=1)
        inputs['velocity']['label'].grid(row=1, column=2)
        self.in_vel = inputs['velocity']['input']
        self.in_vel.grid(row=1, column=3)

    def _create_control_inputs(self, frame):
        inputs = self._control_inputs(frame)
        inputs['control']['label'].grid(row=1, column=0)
        self.in_control = inputs['control']['input']
        self.in_control.grid(row=1, column=1)
        inputs['value']['label'].grid(row=1, column=2)
        self.in_value = inputs['value']['input']
        self.in_value.grid(row=1, column=3)

    def _create_pitch_wheel_inputs(self, frame):
        inputs = self._pitch_wheel_inputs(frame)
        inputs['value']['label'].grid(row=1, column=0)
        self.in_value = inputs['value']['input']
        self.in_value.grid(row=1, column=1)

    # INPUTS ##################################################################

    def _pitch_wheel_inputs(self, frame):
        inputs = {
            'value': {
                'label': ttk.Label(frame, text='VALUE:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
        }
        inputs['value']['label'].data = {'mido_name': 'pitch'}
        # Default value to 'all'
        inputs['value']['input'].current(0)
        return inputs

    def _control_inputs(self, frame):
        inputs = {
            'control': {
                'label': ttk.Label(frame, text='CONTROL:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
            'value': {
                'label': ttk.Label(frame, text='VALUE:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
        }
        inputs['control']['label'].data = {'mido_name': 'control'}
        inputs['value']['label'].data = {'mido_name': 'value'}
        # Default value to 'all'
        inputs['control']['input'].current(0)
        inputs['value']['input'].current(0)
        return inputs

    def _note_inputs(self, frame):
        inputs = {
            'note': {
                'label': ttk.Label(frame, text='NOTE:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
            'velocity': {
                'label': ttk.Label(frame, text='VELOCITY:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
        }
        inputs['note']['label'].data = {'mido_name': 'note'}
        inputs['velocity']['label'].data = {'mido_name': 'velocity'}
        # Default value to 'all'
        inputs['note']['input'].current(0)
        inputs['velocity']['input'].current(0)
        return inputs

    # def _base_inputs(self, frame):
    #     inputs = {
    #         'ch': {
    #             'label': ttk.Label(frame, text='CH:'),
    #             'input': ttk.Combobox(frame,
    #                                   values=self.RANGE_16,
    #                                   state='readonly',
    #                                   width=4),
    #         },
    #         'type': {
    #             'label': ttk.Label(frame, text='TYPE:'),
    #             'input': ttk.Combobox(frame,
    #                                   values=self.TYPES,
    #                                   state='readonly',
    #                                   width=17)
    #         },
    #     }
    #     inputs['ch']['label'].data = {'mido_name': 'channel'}
    #     inputs['type']['label'].data = {'mido_name': 'type'}
    #     # Default value to 'all'
    #     inputs['ch']['input'].current(0)
    #     inputs['type']['input'].current(0)
    #     return inputs

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
