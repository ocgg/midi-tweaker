from .menu_controller import MenuController
from .tabs_container_controller import TabsContainerController


class ApplicationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.tabs_container_controller = TabsContainerController(
            self, model, view)
        self.menu_controller = MenuController(self, model, view)

    def start(self):
        self.view.start_mainloop()
