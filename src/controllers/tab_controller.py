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
        keys_to_remove = {'in': [], 'out': []}

        same_type = in_msg_inputs.get('type') == out_msg_inputs.get('type')

        for key, value in out_msg_inputs.items():
            same_val = in_msg_inputs.get(key) == value
            is_default = value == 'all/keep'
            in_is_default = in_msg_inputs.get(key) == 'all/keep'
            same_default_val = is_default and in_is_default

            if same_default_val or (same_type and same_val):
                keys_to_remove['in'].append(key)
                keys_to_remove['out'].append(key)
            # Case when note_on/note_off & same value (out value is useless)
            elif not same_type and same_val:
                keys_to_remove['out'].append(key)
            elif is_default:
                keys_to_remove['out'].append(key)

        for key in in_msg_inputs:
            is_default = in_msg_inputs[key] == 'all/keep'
            if is_default and key not in keys_to_remove['in']:
                keys_to_remove['in'].append(key)

        for key in keys_to_remove['in']:
            in_msg_inputs.pop(key)
        for key in keys_to_remove['out']:
            out_msg_inputs.pop(key)
