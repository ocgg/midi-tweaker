from .menu_controller import MenuController
from .tab_controller import TabController


class ApplicationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.tab_controller = TabController(self, model, view)
        self.menu_controller = MenuController(self, model, view)

    def start(self):
        self.view.start_mainloop()
