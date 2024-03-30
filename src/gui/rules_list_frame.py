import tkinter as tk


class RulesListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.add_rule_btn = tk.Button(
            self,
            text='Add Rule',
            command=self.master.display_rule_form
        )
        self.add_rule_btn.pack(expand=True)
