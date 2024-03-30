import tkinter as tk
import tkinter.ttk as ttk


class RuleFormFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text='Route message:').grid(
            row=0,
            column=0,
            columnspan=4)

        tk.Label(self, text='CH:').grid(row=1, column=0)
        in_ch = ttk.Combobox(self, values=[i for i in range(1, 17)], width=3)
        in_ch.grid(row=1, column=1)

        tk.Label(self, text='NOTE:').grid(row=1, column=2)
        in_note = ttk.Combobox(
            self,
            values=[i for i in range(1, 129)],
            width=5)
        in_note.grid(row=1, column=3)

        tk.Label(self, text='To:').grid(row=2, column=0, columnspan=4)

        tk.Label(self, text='CH:').grid(row=3, column=0)
        out_ch = ttk.Combobox(self, values=[i for i in range(1, 17)], width=3)
        out_ch.grid(row=3, column=1)

        tk.Label(self, text='NOTE:').grid(row=3, column=2)
        out_note = ttk.Combobox(
            self,
            values=[i for i in range(1, 129)],
            width=5)
        out_note.grid(row=3, column=3)

        tk.Button(
            self,
            text='OK',
            # command=lambda:
            #     self.master.add_rule(
            #         in_ch.get(),
            #         in_note.get(),
            #         out_ch.get(),
            #         out_note.get())).grid(row=4, column=0, columnspan=4)
            command=self.master.display_rules_list).grid(
                row=4, column=0, columnspan=4)
