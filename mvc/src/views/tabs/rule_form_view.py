import tkinter as tk
import tkinter.ttk as ttk


class RuleFormView(tk.Frame):
    TYPES = ['all', 'note_on', 'note_off', 'control_change', "pitchwheel"]
    RANGE_16 = ['all'] + [i for i in range(1, 17)]
    RANGE_128 = ['all'] + [i for i in range(1, 129)]

    def __init__(self, master):
        super().__init__(master)
        self.TAB = master
        # self.ROUTER = router

        self.in_msg_frame = tk.Frame(self)
        self.out_msg_frame = tk.Frame(self)

        tk.Label(self, text='Route:').pack(side='top')
        self.from_msg_form = self._build_form(self.in_msg_frame)
        self.in_msg_frame.pack(side='top')

        tk.Label(self, text='To:').pack(side='top')
        self.to_msg_form = self._build_form(self.out_msg_frame)
        self.out_msg_frame.pack(side='top')

        self.submit_btn = tk.Button(self, text='OK')
        self.submit_btn.pack(side='bottom')

    # LAYOUT ##################################################################

    def _build_form(self, frame):
        inputs = self._base_inputs(frame)

        inputs['ch']['label'].data = {'mido_name': 'channel'}
        inputs['ch']['label'].grid(row=0, column=0)
        msg_ch = inputs['ch']['input']
        msg_ch.grid(row=0, column=1)

        inputs['type']['label'].data = {'mido_name': 'type'}
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
            if i <= 3:
                continue

            widget.grid_remove()

    def _create_note_inputs(self, frame):
        inputs = self._note_inputs(frame)
        inputs['note']['label'].data = {'mido_name': 'note'}
        inputs['note']['label'].grid(row=1, column=0)
        self.in_note = inputs['note']['input']
        self.in_note.grid(row=1, column=1)
        inputs['velocity']['label'].data = {'mido_name': 'velocity'}
        inputs['velocity']['label'].grid(row=1, column=2)
        self.in_vel = inputs['velocity']['input']
        self.in_vel.grid(row=1, column=3)

    def _create_control_inputs(self, frame):
        inputs = self._control_inputs(frame)
        inputs['control']['label'].data = {'mido_name': 'control'}
        inputs['control']['label'].grid(row=1, column=0)
        self.in_control = inputs['control']['input']
        self.in_control.grid(row=1, column=1)
        inputs['value']['label'].data = {'mido_name': 'value'}
        inputs['value']['label'].grid(row=1, column=2)
        self.in_value = inputs['value']['input']
        self.in_value.grid(row=1, column=3)

    def _create_pitch_wheel_inputs(self, frame):
        inputs = self._pitch_wheel_inputs(frame)
        inputs['value']['label'].data = {'mido_name': 'pitch'}
        inputs['value']['label'].grid(row=1, column=0)
        self.in_value = inputs['value']['input']
        self.in_value.grid(row=1, column=1)

    # INPUTS ##################################################################

    def _pitch_wheel_inputs(self, frame):
        return {
            'value': {
                'label': tk.Label(frame, text='VALUE:'),
                'input': ttk.Combobox(
                    frame,
                    values=self.RANGE_128,
                    state='readonly',
                    width=4),
            },
        }

    def _control_inputs(self, frame):
        return {
            'control': {
                'label': tk.Label(frame, text='CONTROL:'),
                'input': ttk.Combobox(
                    frame,
                    values=self.RANGE_128,
                    state='readonly',
                    width=4),
            },
            'value': {
                'label': tk.Label(frame, text='VALUE:'),
                'input': ttk.Combobox(
                    frame,
                    values=self.RANGE_128,
                    state='readonly',
                    width=4),
            },
        }

    def _note_inputs(self, frame):
        return {
            'note': {
                'label': tk.Label(frame, text='NOTE:'),
                'input': ttk.Combobox(
                    frame,
                    values=self.RANGE_128,
                    state='readonly',
                    width=4),
            },
            'velocity': {
                'label': tk.Label(frame, text='VELOCITY:'),
                'input': ttk.Combobox(
                    frame,
                    values=self.RANGE_128,
                    state='readonly',
                    width=4),
            },
        }

    def _base_inputs(self, frame):
        return {
            'ch': {
                'label': ttk.Label(frame, text='CH:'),
                'input': ttk.Combobox(
                    frame,
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
