from ..views.tabs.tab_view import TabView
from ..models.tab_router import TabRouter


class TabController:
    def __init__(self, controller, model, view):
        self.model = model
        self.view = view
        self.tabs_container = view.frames['tabs_container']

        # self.tabs = {
        #   'MIDI port name': {
        #       'view': <TabView object>,
        #       'router': <TabRouter object>
        #   },
        #   ...
        self.tabs = {}

    def add_tab(self, port_name):
        self.tabs[port_name] = {}

        # Create tab & add it to the view
        tab = TabView(self.tabs_container)
        self.tabs[port_name]['view'] = tab

        split_name = port_name.split(':')[1]
        self.tabs_container.add_tab(tab, split_name)
        # Create tab router & stock it
        self.tabs[port_name]['router'] = TabRouter(tab, port_name)
        self._bind(self.tabs[port_name])

    # BINDINGS ################################################################

    def _bind(self, tab):
        # RULE LIST ##########
        add_rule_btn = tab['view'].frames['list'].add_rule_btn
        add_rule_btn.config(command=lambda: tab['view'].display_rule_form())

        # RULE FORM ##########
        submit_btn = tab['view'].frames['form'].submit_btn
        submit_btn.config(command=lambda:
                          self._on_rule_submit(tab['view'], tab['router']))

    # CALLBACKS ###############################################################

    def _on_rule_submit(self, tab, tab_router):
        in_form_data = tab.frames['form'].in_form.get_form_state()
        out_form_data = tab.frames['form'].out_form.get_form_state()

        tab_router.add_rule(in_form_data, out_form_data)

        tab.frames['list'].update_list(tab_router.rules)
        tab.display_rules_list()
