import tkinter as tk
import tkinter.ttk as ttk


class RuleFormView(tk.Frame):
    ALL = 'all/keep'
    TYPES = [ALL, 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = [ALL] + [i for i in range(1, 17)]
    RANGE_128 = [ALL] + [i for i in range(1, 129)]

    def __init__(self, master):
        super().__init__(master)
        self.TAB = master

        self.in_msg_frame = tk.Frame(self)
        self.out_msg_frame = tk.Frame(self)

        tk.Label(self, text='Route:').pack(side='top')
        self.in_msg_form = self._build_form(self.in_msg_frame)
        self.in_msg_frame.pack(side='top')

        tk.Label(self, text='To:').pack(side='top')
        self.out_msg_form = self._build_form(self.out_msg_frame, True)
        self.out_msg_frame.pack(side='top')

        self.submit_btn = tk.Button(self, text='OK')
        self.submit_btn.pack(side='bottom')

    # LAYOUT ##################################################################

    def _build_form(self, frame, is_for_out_msg=False):
        inputs = self._base_inputs(frame, is_for_out_msg)

        inputs['ch']['label'].grid(row=0, column=0)
        inputs['ch']['input'].grid(row=0, column=1)

        inputs['type']['label'].grid(row=0, column=2)
        msg_type = inputs['type']['input']
        msg_type.grid(row=0, column=3)
        msg_type.bind(
            '<<ComboboxSelected>>',
            lambda event: self._on_type_selected(event, frame, msg_type))

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

    def _pitch_wheel_inputs(self, frame, is_for_out_msg=False):
        inputs = {
            'value': {
                'label': tk.Label(frame, text='VALUE:'),
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

    def _control_inputs(self, frame, is_for_out_msg=False):
        inputs = {
            'control': {
                'label': tk.Label(frame, text='CONTROL:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
            'value': {
                'label': tk.Label(frame, text='VALUE:'),
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

    def _note_inputs(self, frame, is_for_out_msg=False):
        inputs = {
            'note': {
                'label': tk.Label(frame, text='NOTE:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_128,
                                      state='readonly',
                                      width=4),
            },
            'velocity': {
                'label': tk.Label(frame, text='VELOCITY:'),
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

    def _base_inputs(self, frame, is_for_out_msg=False):
        inputs = {
            'ch': {
                'label': ttk.Label(frame, text='CH:'),
                'input': ttk.Combobox(frame,
                                      values=self.RANGE_16,
                                      state='readonly',
                                      width=4),
            },
            'type': {
                'label': ttk.Label(frame, text='TYPE:'),
                'input': ttk.Combobox(frame,
                                      values=self.TYPES,
                                      state='readonly',
                                      width=17)
            },
        }
        inputs['ch']['label'].data = {'mido_name': 'channel'}
        inputs['type']['label'].data = {'mido_name': 'type'}
        # Default value to 'all'
        inputs['ch']['input'].current(0)
        inputs['type']['input'].current(0)
        return inputs
