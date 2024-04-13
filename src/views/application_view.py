from .root import Root
from .menu_view import MenuView
from .home_view import HomeView
from .tabs_container_view import TabsContainerView
from ..application_style import ApplicationStyle


class ApplicationView:
    def __init__(self):
        self.root = Root()
        self.style = ApplicationStyle(self.root)
        self.frames = {}

        self.app_menu = MenuView(self.root)
        self.root.config(menu=self.app_menu)

        # FRAMES ######################

        self.frames['home'] = HomeView(self.root)
        self.frames['tabs_container'] = TabsContainerView(self.root)

        # INIT ########################
        self.frames['home'].tkraise()

        # LAYOUT ######################

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky='nsew')

    # MAIN LOOP ###############################################################

    def start_mainloop(self):
        self.root.mainloop()
