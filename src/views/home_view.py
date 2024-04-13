import tkinter.ttk as ttk


class HomeView(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.label = ttk.Label(self, text="Open a new tab to start...",
                               anchor='center')
        self.label.pack(fill='both', expand=True)
