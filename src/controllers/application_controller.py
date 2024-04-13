from .menu_controller import MenuController
from .tabs_container_controller import TabsContainerController


class ApplicationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        tabs_container_view = self.view.frames['tabs_container']
        self.tabs_container_controller = TabsContainerController(
            tabs_container_view)

        self.menu_controller = MenuController(self, model, view)

    def start(self):
        self.view.start_mainloop()
