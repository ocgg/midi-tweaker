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
        out_msg_inputs = self._get_inputs(out_msg_frame, in_msg_inputs)
        print('in msg input: ', in_msg_inputs)
        for k, v in in_msg_inputs.items():
            print(v)
            if v == ['all∕keep']:
                del in_msg_inputs[k]
        print('in msg input: ', in_msg_inputs)
        print('out msg input: ', out_msg_inputs)

        tab_router.add_rule(in_msg_inputs, out_msg_inputs)

        tab.frames['list'].update_list(tab_router.rules)
        tab.display_rules_list()

    def _get_inputs(self, frame, in_msg_inputs=None):
        inputs = {}
        widgets = frame.winfo_children()
        for i in widgets:
            print(i.get()) if i.winfo_class() == 'TCombobox' else None

        for i, widget in enumerate(widgets):
            # skips labels & default values
            if self._is_label_or_default_value(widget):
                continue

            value = widget.get()
            value = [int(value)-1] if value.isdigit() else [value]
            attribute = widgets[i-1].data['mido_name']

            inputs[attribute] = value

        return inputs

    def _is_label_or_default_value(self, widget):
        try:
            return widget.get() == 'all/keep'
        except AttributeError:
            return True
