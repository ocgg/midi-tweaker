from ._rule_form_frame import RuleFormFrame
import tkinter.ttk as ttk


class RuleFormView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # IN FORM #####################
        self.in_form = RuleFormFrame(self, 'in')

        # OUT FORM ####################
        self.out_form = RuleFormFrame(self, 'out')

        # SEPARATOR ###################
        separator = ttk.Frame(self)
        separator.rowconfigure(0, weight=1)
        separator.rowconfigure(2, weight=1)

        sep_1 = ttk.Separator(separator, orient='vertical')
        sep_label = ttk.Label(separator, text='⮕')
        sep_2 = ttk.Separator(separator, orient='vertical')

        sep_1.grid(row=0, column=0, sticky='ns', pady=(10, 0))
        sep_label.grid(row=1, column=0)
        sep_2.grid(row=2, column=0, sticky='ns', pady=(0, 10))

        # BUTTONS #####################
        buttons_container = ttk.Frame(self)
        buttons_container.rowconfigure(0, weight=1)
        buttons_container.columnconfigure(0, weight=1, uniform='buttons')
        buttons_container.columnconfigure(2, weight=1, uniform='buttons')

        self.cancel_btn = ttk.Button(buttons_container, text='Cancel')
        self.submit_btn = ttk.Button(buttons_container, text='Done')
        self.cancel_btn.config(style='cancel.TButton')
        self.submit_btn.config(style='big.TButton')

        self.cancel_btn.grid(row=0, column=0, sticky='e')
        self.submit_btn.grid(row=0, column=1)

        # LAYOUT ######################
        self.columnconfigure(0, weight=1, uniform='form_frame')
        self.columnconfigure(2, weight=1, uniform='form_frame')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Row 0
        self.in_form.grid(row=0, column=0, sticky='nsew')
        separator.grid(row=0, column=1, sticky='ns')
        self.out_form.grid(row=0, column=2, sticky='nsew')

        # Row 1
        buttons_container.grid(row=1, column=0, columnspan=3,
                               sticky='ew', pady=(0, 10))
