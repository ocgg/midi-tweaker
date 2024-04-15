import tkinter.ttk as ttk


class TabsContainerView(ttk.Frame):
    def __init__(self, view):
        super().__init__(view)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def add_and_display_tab(self, tab, name):
        self.add(tab, text=name)
        self.select(tab)

    # TEMPORARY #######################
    # Use it till the return of the mighty tabs functionality
    # And then delete it and show no mercy
    def bypass_tabs(self, tab_view):
        tab_view.grid(row=0, column=0, sticky='nsew')
    # /TEMPORARY ######################
