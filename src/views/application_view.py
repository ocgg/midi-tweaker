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

        self._add_frame(TabsContainerView, "tabs_container")
        self._add_frame(HomeView, "home")

    # PRIVATE ##########

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    # INIT ##########

    def start_mainloop(self):
        self.root.mainloop()
