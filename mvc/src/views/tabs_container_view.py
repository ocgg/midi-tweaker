import tkinter.ttk as ttk


class TabsContainerView(ttk.Notebook):
    def __init__(self, view):
        super().__init__(view)
        # self.tabs = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def add_tab(self, tab, name):
        self.add(tab, text=name)
        # self.tabs[port_name] = tab
        self.select(tab)
