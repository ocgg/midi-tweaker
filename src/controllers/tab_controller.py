from ..views.tabs.tab_view import TabView
from ..models.tab_router import TabRouter


class TabController:
    def __init__(self, controller, model, view):
        self.model = model
        self.view = view
        self.tabs_container = view.frames['tabs_container']

        self.tab_routers = {}

    def add_tab(self, port_name):
        # Create tab & add it to the view
        tab = TabView(self.tabs_container)
        split_name = port_name.split(':')[1]
        self.tabs_container.add_tab(tab, split_name)
        # Create tab router & stock it
        self.tab_routers[port_name] = TabRouter(tab, port_name)
        self._bind(tab, self.tab_routers[port_name])

    # BINDINGS ################################################################

    def _bind(self, tab, tab_router):
        # RULE LIST ##########
        # Add new rule btn
        add_rule_btn = tab.frames['list'].add_rule_btn
        add_rule_btn.config(command=lambda: tab.display_rule_form())

        # RULE FORM ##########
        # Submit btn
        submit_btn = tab.frames['form'].submit_btn
        submit_btn.config(command=lambda:
                          self._on_rule_submit(tab, tab_router))

    # CALLBACKS ###############################################################

    def _on_rule_submit(self, tab, tab_router):
        in_msg_frame = tab.frames['form'].in_msg_frame
        out_msg_frame = tab.frames['form'].out_msg_frame

        in_msg_inputs = self._get_inputs(in_msg_frame)
        out_msg_inputs = self._get_inputs(out_msg_frame)

        tab_router.add_rule(in_msg_inputs, out_msg_inputs)

        tab.frames['list'].update_list(tab_router.rules)
        tab.display_rules_list()

    def _get_inputs(self, frame):
        inputs = {}
        for i, widget in enumerate(frame.winfo_children()):
            if i % 2 == 0:
                value = frame.winfo_children()[i+1].get()
                if value and value != 'all':
                    label = widget.data['mido_name']
                    inputs[label] = int(value)-1 if value.isdigit() else value
        return inputs
