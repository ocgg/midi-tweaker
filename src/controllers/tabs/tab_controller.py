from .rules_list_controller import RulesListController
from .rule_form_controller import RuleFormController
from src.modules.constants import (
    PORT_CHOICE_NONE,
    PORT_CHOICE_ALL,
    PORT_CHOICE_NEW,
)


class TabController:
    def __init__(self, tab_view, tab_router):
        self.view = tab_view
        self.router = tab_router

        self.rules_list_controller = RulesListController(
            tab_controller=self,
            view=self.view.frames['list'],
            router=tab_router)

        self.rule_form_controller = RuleFormController(
            tab_controller=self,
            view=self.view.frames['form'],
            router=tab_router)

        self._bind()

    # LIST/FORM COORDINATION ##################################################

    def update_rules_list(self):
        self.rules_list_controller.update_list()

    def show_rules_list(self):
        self.view.display_rules_list()

    def show_rule_form(self):
        self.view.display_rule_form()

    # BINDINGS ################################################################

    def _bind(self):
        # MIDI BARS ###################
        # Port list comboboxes & refresh buttons
        self._bind_midi_bar('in')
        self._bind_midi_bar('out')

    def _bind_midi_bar(self, source):
        # Set midi ports list for comboboxes
        midi_ports = self.router.get_midi_ports(source)
        combobox = self.view.midi_bars[source]['ports']['combobox']
        self.view.update_midi_ports(source, midi_ports)
        combobox.bind('<<ComboboxSelected>>',
                      lambda event: self._on_port_selected(source, combobox))
        # Refresh button
        refresh_btn = self.view.midi_bars[source]['ports']['refresh']
        refresh_btn.config(command=lambda: self._on_ports_refresh(source))

    def _bind_create_port_btn(self):
        self.view.create_port_btn.config(
            command=self._on_create_virtual_out_port)

    # CALLBACKS ###############################################################

    # MIDI bar ports ######################################
    def _on_port_selected(self, source, combobox):
        port_name = combobox.get()
        if port_name == PORT_CHOICE_ALL:
            self.router.set_input_ports_all()
        elif port_name == PORT_CHOICE_NONE:
            self.router.close_midi_ports(source)
        elif port_name == PORT_CHOICE_NEW:
            # Open dialog to create new port and ask a port name (view)
            self.view.ask_new_port_name()
            self._bind_create_port_btn()
        else:
            self.router.set_midi_port(source, port_name)

    def _on_ports_refresh(self, source):
        midi_ports = self.router.get_midi_ports(source)
        self.view.update_midi_ports(source, midi_ports)

    def _on_create_virtual_out_port(self):
        # get new out port name (view)
        name = self.view.new_port_entry.get()
        # create virtual out port with name (router)
        self.router.create_virtual_out(name)
        self.view.update_midi_ports('out', self.router.get_midi_ports('out'))
        # select the new port in the combobox (view)
        combobox = self.view.midi_bars['out']['ports']['combobox']
        combobox.set(name)
        # close the dialog (view)
        self.view.new_port_toplevel.destroy()
