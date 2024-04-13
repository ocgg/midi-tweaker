from src.models.rule import Rule
from src.modules.constants import (
    MIDO_TYPE_TO_VALUES,
    MIDO_ATTR_RANGE
)


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

    # MIDI Learn ##########################################
    def _on_midi_learn(self, source, learn_btn):
        self.router.learn(source)
        learn_btn.config(command=lambda:
                         self._on_stop_midi_learn(source, learn_btn))

    def _on_stop_midi_learn(self, source, learn_btn):
        self.router.stop_learn(source)
        learn_btn.config(command=lambda:
                         self._on_midi_learn(source, learn_btn))

    # MIDI bar refresh ports ##############################
    def _on_refresh(self, source):
        midi_ports = self.router.get_midi_ports(source)
        self.view.update_midi_ports(source, midi_ports)

    # Rule form submit ####################################
    def _on_rule_submit(self):
        # Stop midi_learn if active
        if self.router.learn_is_active:
            self.router.stop_learn('in')
            self.router.stop_learn('out')

        in_form_inputs = self.view.frames['form'].in_form.inputs
        out_form_inputs = self.view.frames['form'].out_form.inputs

        # validate form data
        validation = self._validate_form_data(in_form_inputs, out_form_inputs)
        is_valid = validation[0]
        in_form_data = validation[1]
        out_form_data = validation[2]

        if is_valid:
            rule = Rule(in_form_data, out_form_data)
            self.router.add_rule(rule)
            self.view.frames['list'].update_list(self.router.rules)
            self.view.display_rules_list()
        else:
            self.view.frames['form'].in_form.display_errors(in_form_data)
            self.view.frames['form'].out_form.display_errors(out_form_data)

    def _validate_form_data(self, in_form_inputs, out_form_inputs):
        is_valid = True
        in_form_data = self._process_form_data(in_form_inputs)
        out_form_data = self._process_form_data(out_form_inputs)
        # Should convert value types (int & list)
        # Return a tuple (False, in_form_data, out_form_data) if invalid
        # with error messages in place of input values for the view to display
        # Or (True, in_form_data, out_form_data) if valid

        # VALIDATIONS #################
        # These data are in MIDO_ATTR_RANGE constant
        # - channel between 1 and 16
        # - pitch between -8192 and 8191
        # - other values between 0 and 127
        #
        # - Out form should not be empty
        # - ...

        for value in in_form_data.values():
            if not value:
                is_valid = False
        for value in out_form_data.values():
            if not value:
                is_valid = False

        return (is_valid, in_form_data, out_form_data)

    def _process_form_data(self, form_inputs):
        form_data = {}
        form_data['channel'] = form_inputs['channel'].get().replace(' ', '')
        form_data['type'] = form_inputs['type'].get().replace(' ', '')

        # TODO: refacto. Only one for loop

        # Get type's input (val1, val2) values if type selected
        values_names = MIDO_TYPE_TO_VALUES.get(form_data['type']) or []
        for value in values_names:
            form_data[value] = form_inputs[value].get().replace(' ', '')
        # Remove empty values
        form_data = {k: v for k, v in form_data.items() if v}
        # convert to int in list or to range
        for key, value in form_data.items():
            if value.isdigit():
                form_data[key] = self._check_int_conversion(key, value)
            else:
                form_data[key] = self._check_range_conversion(key, value)

        return form_data

    def _check_int_conversion(self, key, value):
        value = int(value)
        if value in MIDO_ATTR_RANGE[key]:
            return value
        else:
            return False

    def _check_range_conversion(self, key, value):
        try:
            range_vals = list(map(int, value.split('-')))
            return range(range_vals[0], range_vals[1] + 1)
        except ValueError:
            return False
