from ..views.tabs.tab_view import TabView
from .tabs.tab_router import TabRouter
from .tabs.tab_controller import TabController


class TabsContainerController:
    def __init__(self, tabs_container_view):
        self.view = tabs_container_view
        self.tabs = {}

    def add_tab(self, tab_name):
        self.tabs[tab_name] = {}

        # Instantiate all tab's components
        tab_view = TabView(self.view)
        tab_router = TabRouter(tab_view, tab_name)
        tab_controller = TabController(tab_view, tab_router)

        # Stock tab
        tab = self.tabs[tab_name]
        tab['view'] = tab_view
        tab['router'] = tab_router
        tab['controller'] = tab_controller

        # Add tab to the view
        self.view.add_and_display_tab(tab_view, tab_name)
