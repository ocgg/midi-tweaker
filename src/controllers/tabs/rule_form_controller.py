from src.models.rule import Rule
from src.modules.constants import FORM_ATTR_RANGE, MIDO_BYTE2_NAMES


class RuleFormController:
    def __init__(self, tab_controller, view, router):
        self.tab_controller = tab_controller
        self.view = view
        self.in_form = view.forms['in']
        self.out_form = view.forms['out']
        self.router = router
        self._bind()

    # BINDINGS ################################################################

    def _bind(self):
        # Cancel button
        cancel_btn = self.view.cancel_btn
        cancel_btn.config(command=self.tab_controller.show_rules_list)
        # Submit button
        submit_btn = self.view.submit_btn
        submit_btn.config(command=self._on_rule_submit)
        # Learn buttons
        in_learn_btn = self.in_form.learn_btn
        out_learn_btn = self.out_form.learn_btn
        in_learn_btn.config(command=lambda:
                            self._on_midi_learn('in', in_learn_btn))
        out_learn_btn.config(command=lambda:
                             self._on_midi_learn('out', out_learn_btn))

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

    # Submit ##############################################

    def _on_rule_submit(self):
        # Stop midi_learn if active
        if self.router.learn_is_active:
            self.router.stop_learn('in')
            self.router.stop_learn('out')
        # Clear error labels
        self.in_form.clear_errors()
        self.out_form.clear_errors()

        in_form_data = self.in_form.form_data
        out_form_data = self.out_form.form_data

        # validate form data
        validation = self._validate_form_data(in_form_data, out_form_data)
        # is_valid = validation[0]
        # in_form_data = validation[1]
        # out_form_data = validation[2]

        if validation['is_ok']:
            rule = Rule(in_form_data, out_form_data)
            self.router.add_rule(rule)
            self.view.clear_forms()
            self.tab_controller.update_rules_list()
            self.tab_controller.show_rules_list()
        elif validation['error_source'] == 'global':
            self.out_form.display_global_error()
        else:
            self.in_form.display_field_errors(in_form_data)
            self.out_form.display_field_errors(out_form_data)

    # FORM VALIDATION #########################################################

    def _validate_form_data(self, in_form_data, out_form_data):
        # FIELDS VALIDATIONS ##########
        # Validations that concern only in or out form independently
        # VALIDATES: values should be in right range
        # VALIDATES: ranges should be written in right format
        in_form_data = self._process_form_data(in_form_data)
        out_form_data = self._process_form_data(out_form_data)

        # CHECKPOINT #################
        is_valid = all(in_form_data.values()) and all(out_form_data.values())
        if not is_valid:
            return {'is_ok': False, 'error_source': 'field'}

        # GLOBAL VALIDATIONS ##########
        # Validations between both forms

        # VALIDATES: rule should change original input
        in_form_set = set(in_form_data.keys())
        out_form_set = set(out_form_data.keys())
        sets_intersection = in_form_set.intersection(out_form_set)
        intersection = {key: in_form_data[key] for key in sets_intersection}
        out_dont_change = intersection == out_form_data
        if out_dont_change:
            return {'is_ok': False, 'error_source': 'global'}

        # VALIDATION OK FROM HERE #####

        # Remove type key if same
        in_type = in_form_data.get('type')
        out_type = out_form_data.get('type')
        same_type = in_type == out_type and out_type is not None
        if same_type:
            del in_form_data['type']
            del out_form_data['type']

        for key, value in out_form_data.items():
            # if out is range and in empty, in should be whole range
            if isinstance(value, range) and not in_form_data.get(key):
                in_form_data[key] = FORM_ATTR_RANGE[key]

        return {'is_ok': True}

    def _process_form_data(self, form_data):
        # Convert to [int] or to range
        for key, value in form_data.items():
            if key == 'type':
                continue
            elif value.isdigit():
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
