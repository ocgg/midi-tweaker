from src.models.rule import Rule
from src.modules.constants import (
    MIDO_TYPE_TO_VALUES,
    MIDO_ATTR_RANGE,
    FORM_ATTR_RANGE,
)


class TabController:
    def __init__(self, tab_view, tab_router):
        self.view = tab_view
        self.router = tab_router
        self.form_frame = self.view.frames['form']
        self.list_frame = self.view.frames['list']

        self._bind()

    # BINDINGS ################################################################

    def _bind(self):
        # MIDI BARS ###################
        # Port list comboboxes & refresh buttons
        self._bind_midi_bar('in')
        self._bind_midi_bar('out')

        # RULE LIST ###################
        # Add rule button
        add_rule_btn = self.list_frame.add_rule_btn
        add_rule_btn.config(command=lambda: self.view.display_rule_form())

        # RULE FORM ###################
        # Submit button
        submit_btn = self.form_frame.submit_btn
        submit_btn.config(command=self._on_rule_submit)
        # Learn buttons
        in_learn_btn = self.form_frame.in_form.learn_btn
        out_learn_btn = self.form_frame.out_form.learn_btn
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
        refresh_btn.config(command=lambda: self._on_ports_refresh(source))

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
    def _on_ports_refresh(self, source):
        midi_ports = self.router.get_midi_ports(source)
        self.view.update_midi_ports(source, midi_ports)

    # Rule form submit ####################################
    def _on_rule_submit(self):
        # Stop midi_learn if active
        if self.router.learn_is_active:
            self.router.stop_learn('in')
            self.router.stop_learn('out')

        # in_form_inputs = self.form_frame.in_form.inputs
        # out_form_inputs = self.form_frame.out_form.inputs
        in_form_data = self.form_frame.in_form.form_data
        out_form_data = self.form_frame.out_form.form_data

        # validate form data
        validation = self._validate_form_data(in_form_data, out_form_data)
        is_valid = validation[0]
        in_form_data = validation[1]
        out_form_data = validation[2]

        if is_valid:
            rule = Rule(in_form_data, out_form_data)
            self.router.add_rule(rule)
            self.list_frame.update_list(self.router.rules)
            self.view.display_rules_list()
        elif not out_form_data:
            self.form_frame.out_form.display_global_error()
        else:
            self.form_frame.in_form.display_field_errors(in_form_data)
            self.form_frame.out_form.display_field_errors(out_form_data)

    def _validate_form_data(self, in_form_data, out_form_data):
        # VALIDATIONS #####################################
        # On only one form's part #####
        # These data are in FORM_ATTR_RANGE constant
        # - channel between 1 and 16
        # - pitch between -8192 and 8191
        # - other values between 0 and 127

        # On both forms ###############
        # - Out form should not be empty
        # - ...

        # FIELD VALIDATIONS ###############################

        # Convert and validates data types (values & ranges values)
        in_form_data = self._process_form_data(in_form_data)
        out_form_data = self._process_form_data(out_form_data)

        # CHECKPOINT ######################################
        is_valid = all(in_form_data.values()) and all(out_form_data.values())
        if not is_valid:
            return (is_valid, in_form_data, out_form_data)

        # BOTH FORMS VALIDATIONS ##########################

        # Remove values that are equal in both forms
        key_to_remove = []
        for key, value in in_form_data.items():
            if out_form_data.get(key) and value == out_form_data[key]:
                key_to_remove.append(key)
        for key in key_to_remove:
            del in_form_data[key]
            del out_form_data[key]

        if not out_form_data:
            is_valid = False

        return (is_valid, in_form_data, out_form_data)

    def _process_form_data(self, form_data):
        # Convert to [int] or to range
        for key, value in form_data.items():
            if value.isdigit():
                form_data[key] = self._check_int_conversion(key, value)
            else:
                form_data[key] = self._check_range_conversion(key, value)
        return form_data

    def _check_int_conversion(self, key, value):
        value = int(value)
        if value in FORM_ATTR_RANGE[key]:
            return [value]
        else:
            return False

    def _check_range_conversion(self, key, value):
        try:
            range_vals = list(map(int, value.split('-')))
            min = range_vals[0]
            max = range_vals[1]
            # Let the user have twisted logic
            min, max = (min, max) if min < max else (max, min)
            min_is_valid = min in FORM_ATTR_RANGE[key]
            max_is_valid = max in FORM_ATTR_RANGE[key]
            # Do not let the user be irrational
            if not min_is_valid or not max_is_valid:
                return False
            # Let the user be distracted
            elif min == max:
                return [min]
            else:
                return range(min, max + 1)
        except ValueError:
            return False
