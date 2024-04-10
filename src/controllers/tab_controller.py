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

    def add_tab(self, tab_name):
        self.tabs[tab_name] = {}

        # Create tab & add it to the view
        tab = TabView(self.tabs_container)
        self.tabs[tab_name]['view'] = tab
        self.tabs_container.add_tab(tab, tab_name)

        # Create tab router & stock it
        self.tabs[tab_name]['router'] = TabRouter(tab, tab_name)
        self._bind(self.tabs[tab_name])

    # BINDINGS ################################################################

    def _bind(self, tab):
        tab_view = tab['view']
        tab_router = tab['router']

        # MIDI BARS ###################
        self._bind_midi_bar(tab, 'in')
        self._bind_midi_bar(tab, 'out')

        # RULE LIST ###################
        add_rule_btn = tab_view.frames['list'].add_rule_btn
        add_rule_btn.config(command=lambda: tab_view.display_rule_form())

        # RULE FORM ###################
        submit_btn = tab_view.frames['form'].submit_btn
        submit_btn.config(command=lambda:
                          self._on_rule_submit(tab_view, tab_router))

    def _bind_midi_bar(self, tab, source):
        tab_view = tab['view']
        tab_router = tab['router']
        # Set midi ports list for comboboxes
        midi_ports = tab_router.get_midi_ports(source)
        combobox = tab_view.midi_bars[source]['ports']['combobox']
        combobox['values'] += tuple(midi_ports)
        combobox.bind(
            '<<ComboboxSelected>>',
            lambda event:
                tab_router.set_midi_port(event, source, combobox.get())
        )
        # Refresh button
        refresh_btn = tab_view.midi_bars[source]['ports']['refresh']
        refresh_btn.config(command=lambda: self._on_refresh(tab, source))

    # CALLBACKS ###############################################################

    def _on_refresh(self, tab, source):
        print
        midi_ports = tab['router'].get_midi_ports(source)
        tab['view'].update_midi_ports(source, midi_ports)

    def _on_rule_submit(self, tab_view, tab_router):
        in_form_data = tab_view.frames['form'].in_form.get_form_state()
        out_form_data = tab_view.frames['form'].out_form.get_form_state()
        self._clear_inputs(in_form_data, out_form_data)

        tab_router.add_rule(in_form_data, out_form_data)

        tab_view.frames['list'].update_list(tab_router.rules)
        tab_view.display_rules_list()

    def _clear_inputs(self, in_form_data, out_form_data):
        # Removes useless keys in both form_data
        keys_to_remove = {'in': [], 'out': []}

        same_type = in_form_data.get('type') == out_form_data.get('type')
        for key, value in out_form_data.items():
            same_val = in_form_data.get(key) == value
            # CONDITIONS ORDER IS IMPORTANT
            if same_type and key == 'type':
                keys_to_remove['out'].append(key)
            elif same_type and same_val:
                keys_to_remove['in'].append(key)
                keys_to_remove['out'].append(key)
            elif not same_type and same_val:
                # Case when note_on/note_off & same value
                keys_to_remove['out'].append(key)

        for key in keys_to_remove['in']:
            in_form_data.pop(key)
        for key in keys_to_remove['out']:
            out_form_data.pop(key)
