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
        add_rule_btn = tab.frames['list'].add_rule_btn
        add_rule_btn.config(command=lambda: tab.display_rule_form())

        # RULE FORM ##########
        submit_btn = tab.frames['form'].submit_btn
        submit_btn.config(command=lambda:
                          self._on_rule_submit(tab, tab_router))

    # CALLBACKS ###############################################################

    def _on_rule_submit(self, tab, tab_router):
        in_msg_frame = tab.frames['form'].in_msg_frame
        out_msg_frame = tab.frames['form'].out_msg_frame

        in_msg_inputs = self._get_inputs(in_msg_frame)
        out_msg_inputs = self._get_inputs(out_msg_frame)
        self._clear_inputs(in_msg_inputs, out_msg_inputs)

        tab_router.add_rule(in_msg_inputs, out_msg_inputs)

        tab.frames['list'].update_list(tab_router.rules)
        tab.display_rules_list()

    def _get_inputs(self, frame):
        inputs = {}
        widgets = frame.winfo_children()

        for i, widget in enumerate(widgets):
            # skips labels
            try:
                value = widget.get()
            except AttributeError:
                continue
            value = int(value)-1 if value.isdigit() else value
            attribute = widgets[i-1].data['mido_name']
            inputs[attribute] = value
        return inputs

    def _clear_inputs(self, in_msg_inputs, out_msg_inputs):
        # Handle note_on and note_off as the same type
        in_type = in_msg_inputs['type']
        out_type = out_msg_inputs['type']
        same_types = in_type == out_type
        if not same_types and 'note' in in_type and 'note' in out_type:
            same_types = True
        # removes all key with the same value in both for ch and type
        for key in list(in_msg_inputs.keys()):
            has_same_value = in_msg_inputs[key] == out_msg_inputs[key]
            if not same_types and has_same_value:
                in_msg_inputs.pop(key)
                out_msg_inputs.pop(key)
        # removes all key with value 'all/keep'
        for k, v in list(in_msg_inputs.items()):
            if v == 'all/keep':
                in_msg_inputs.pop(k)
        for k, v in list(out_msg_inputs.items()):
            if v == 'all/keep':
                out_msg_inputs.pop(k)
