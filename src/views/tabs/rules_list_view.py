import tkinter as tk


class RulesListView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.add_rule_btn = tk.Button(self, text='Add Rule')
        self.add_rule_btn.pack(expand=True)

    def update_list(self, rules):
        self.add_rule_btn.pack_forget()
        for rule in rules:
            rule_frame = tk.Frame(self)
            tk.Label(rule_frame, text=rule.from_msg).pack(side='left')
            tk.Label(rule_frame, text='➞').pack(side='left')
            tk.Label(rule_frame, text=rule.to_msg).pack(side='left')
            rule_frame.pack()
        self.add_rule_btn.pack(expand=True)
