class MenuController:
    def __init__(self, controller, model, view):
        self.model = model
        self.view = view
        self.tab_controller = controller.tab_controller

        self.app_menu = view.app_menu
        self.tabs_container = view.frames["tabs_container"]

        self.file_menu = self.app_menu.file_menu
        self.ports_menu = self.app_menu.ports_menu

        self.midi_ports = self.model.midi_port.all()
        self.app_menu.build_ports_menu(self.midi_ports)

        self._bind()

    # BINDINGS ################################################################

    def _bind(self):
        # FILE Menu ##########

        self.file_menu.entryconfig('Quit', command=self.view.root.quit)

        # MIDI PORTS Menu ##########

        self.ports_menu.entryconfig('Refresh', command=self._refresh_ports)
        # MIDI ports choice
        for i, port in enumerate(self.midi_ports):
            self.ports_menu.entryconfig(
                i + 2, command=lambda port=port: self._open_tab(port))

    # CALLBACKS ###############################################################

    def _refresh_ports(self):
        # Clear all entries except "Refresh" and separator
        self.app_menu.ports_menu.delete(2, "end")

        self.midi_ports = self.model.midi_port.all()
        self.app_menu.build_ports_menu(self.midi_ports)

    def _open_tab(self, port):
        self.tabs_container.tkraise()
        self.tab_controller.add_tab(port)
