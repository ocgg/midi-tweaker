import tkinter as tk
import tkinter.ttk as ttk


class RulesListView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.add_rule_btn = tk.Button(self, text='Add Rule')
        self.add_rule_btn.pack(expand=True)

    def update_list(self, rules):
        self.add_rule_btn.pack_forget()
        for rule in rules:
            rule_frame = tk.Frame(self)
            tk.Label(rule_frame, text=rule.in_attrs).pack(side='left')
            tk.Label(rule_frame, text='➞').pack(side='left')
            tk.Label(rule_frame, text=rule.out_attrs).pack(side='left')
            rule_frame.pack()
        self.add_rule_btn.pack(expand=True)
        note_txt = ('Note: rules apply one by one in order. One rule is '
                    'skipped if it cannot apply to the message being routed '
                    'AND to the original MIDI IN message.')
        note = ttk.Label(self, text=note_txt, foreground='gray',
                         wraplength=450, justify='center')
        note.pack(side='bottom')
