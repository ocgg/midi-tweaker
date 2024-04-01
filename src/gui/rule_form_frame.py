import tkinter as tk
import tkinter.ttk as ttk


class RuleFormFrame(tk.Frame):
    def __init__(self, master, router):
        super().__init__(master)
        self.TAB = master
        self.ROUTER = router

        tk.Label(self, text='Route:').grid(row=0, column=0, columnspan=4)

        self.from_msg = {}
        for i, (key, value) in enumerate(self._create_inputs().items()):
            value['label'].grid(row=1, column=i*2)
            value['input'].grid(row=1, column=i*2+1)
            self.from_msg[key] = value['input']

        tk.Label(self, text='To:').grid(row=2, column=0, columnspan=4)

        self.to_msg = {}
        for i, (key, value) in enumerate(self._create_inputs().items()):
            value['label'].grid(row=3, column=i*2)
            value['input'].grid(row=3, column=i*2+1)
            self.to_msg[key] = value['input']

        tk.Button(
            self,
            text='OK',
            command=self._print_test
        ).grid(row=4, column=0, columnspan=4)

    # PRIVATE METHODS #########################################################

    def _print_test(self):
        print('From:')
        for key, value in self.from_msg.items():
            print(key, value.get())
        print('To:')
        for key, value in self.to_msg.items():
            print(key, value.get())

    def _create_inputs(self):
        return {
            'ch': {
                'label': ttk.Label(self, text='CH:'),
                'input': ttk.Combobox(
                    self,
                    values=[i for i in range(1, 17)],
                    width=4),
            },
            'type': {
                'label': ttk.Label(self, text='TYPE:'),
                'input': ttk.Combobox(
                    self,
                    values=['NOTE_ON', 'NOTE_OFF', 'CONTROL_CHANGE'],
                    width=17),
            },
            'type_nbr': {
                'label': ttk.Label(self, text='NBR:'),
                'input': ttk.Combobox(
                    self,
                    values=[i for i in range(1, 129)],
                    width=5),
            },
            'value': {
                'label': ttk.Label(self, text='VALUE:'),
                'input': ttk.Combobox(
                    self,
                    values=[i for i in range(1, 129)],
                    width=5),
            },
        }
