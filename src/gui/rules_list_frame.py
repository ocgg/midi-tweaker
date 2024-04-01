import tkinter as tk


class RulesListFrame(tk.Frame):
    def __init__(self, master, router):
        super().__init__(master)
        self.TAB = master
        self.rules = self.TAB.ROUTER.rules

        self.add_rule_btn = tk.Button(
            self,
            text='Add Rule',
            command=self.TAB.display_rule_form
        )
        self.add_rule_btn.pack(expand=True)

    def update(self):
        self.add_rule_btn.pack_forget()
        for rule in self.rules:
            rule_frame = tk.Frame(self)
            tk.Label(rule_frame, text=rule.from_msg).pack(side='left')
            tk.Label(rule_frame, text='➞').pack(side='left')
            tk.Label(rule_frame, text=rule.to_msg).pack(side='left')
            rule_frame.pack()
        self.add_rule_btn.pack(expand=True)
