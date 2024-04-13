from src.models.rule import Rule


class TabController:
    def __init__(self, tab_view, tab_router):
        self.view = tab_view
        self.router = tab_router

        self._bind()

    # BINDINGS ################################################################

    def _bind(self):
        # MIDI BARS ###################
        # Port list comboboxes & refresh buttons
        self._bind_midi_bar('in')
        self._bind_midi_bar('out')

        # RULE LIST ###################
        # Add rule button
        add_rule_btn = self.view.frames['list'].add_rule_btn
        add_rule_btn.config(command=lambda: self.view.display_rule_form())

        # RULE FORM ###################
        # Submit button
        submit_btn = self.view.frames['form'].submit_btn
        submit_btn.config(command=self._on_rule_submit)
        # Learn buttons
        in_learn_btn = self.view.frames['form'].in_form.learn_btn
        out_learn_btn = self.view.frames['form'].out_form.learn_btn
        in_learn_btn.config(command=lambda:
                            self._on_midi_learn('in', in_learn_btn))
        out_learn_btn.config(command=lambda:
                             self._on_midi_learn('out', out_learn_btn))

    def _bind_midi_bar(self, source):
        # Set midi ports list for comboboxes
        midi_ports = self.router.get_midi_ports(source)
        combobox = self.view.midi_bars[source]['ports']['combobox']
        combobox['values'] += tuple(midi_ports)
        combobox.bind(
            '<<ComboboxSelected>>',
            lambda event:
                self.router.set_midi_port(event, source, combobox.get())
        )
        # Refresh button
        refresh_btn = self.view.midi_bars[source]['ports']['refresh']
        refresh_btn.config(command=lambda: self._on_refresh(source))

    # CALLBACKS ###############################################################

    # MIDI Learn #####################
    def _on_midi_learn(self, source, learn_btn):
        self.router.learn(source)
        learn_btn.config(command=lambda:
                         self._on_stop_midi_learn(source, learn_btn))

    def _on_stop_midi_learn(self, source, learn_btn):
        self.router.stop_learn(source)
        learn_btn.config(command=lambda:
                         self._on_midi_learn(source, learn_btn))

    # MIDI bar refresh ports ##########
    def _on_refresh(self, source):
        midi_ports = self.router.get_midi_ports(source)
        self.view.update_midi_ports(source, midi_ports)

    # Rule form submit ###############
    def _on_rule_submit(self):
        # Stop midi_learn if active
        if self.router.learn_is_active:
            self.router.stop_learn('in')
            self.router.stop_learn('out')

        in_form_data = self.view.frames['form'].in_form.get_form_data()
        out_form_data = self.view.frames['form'].out_form.get_form_data()

        # validate in_form_data
        #

        self._clear_inputs(in_form_data, out_form_data)

        # TODO: Rule validations

        rule = Rule(in_form_data, out_form_data)
        self.router.add_rule(rule)

        self.view.frames['list'].update_list(self.router.rules)
        self.view.display_rules_list()

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
