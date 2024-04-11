class MenuController:
    def __init__(self, controller, model, view):
        self.model = model
        self.view = view
        self.tab_controller = controller.tab_controller

        self.app_menu = view.app_menu
        self.tabs_container = view.frames["tabs_container"]

        self.file_menu = self.app_menu.file_menu

        self._bind()

    # BINDINGS ################################################################

    def _bind(self):
        # FILE Menu ###################
        self.file_menu.entryconfig('Quit', command=self.view.root.quit)

        # Open tab btn ###############
        self.app_menu.entryconfig('Open tab', command=self._open_tab)

    # CALLBACKS ###############################################################

    def _open_tab(self):
        self.tabs_container.tkraise()
        self.tab_controller.add_tab('New tab')
