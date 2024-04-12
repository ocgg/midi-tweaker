from src.models.application_model import ApplicationModel
from src.views.application_view import ApplicationView
from src.controllers.application_controller import ApplicationController

import mido


def main():
    model = ApplicationModel()
    view = ApplicationView()
    controller = ApplicationController(model, view)

    controller.menu_controller._open_tab()
    test_tab = controller.tab_controller.tabs['New tab']

    port = mido.get_input_names()[0]
    test_tab['view'].midi_bars['in']['ports']['combobox'].set(port)
    test_tab['router'].set_midi_port(None, 'in', port)

    rule1_in = {'type': 'note_on', 'velocity': 0}
    rule1_out = {'type': 'note_off'}
    test_tab['router'].add_rule(rule1_in, rule1_out)

    rule2_in = {'type': 'control_change', 'control': 1}
    rule2_out = {'control': 10}
    test_tab['router'].add_rule(rule2_in, rule2_out)

    rule3_in = {}
    rule3_out = {'channel': 2}
    test_tab['router'].add_rule(rule3_in, rule3_out)

    rule4_in = {'channel': 1, 'type': 'control_change', 'control': 10, 'value': 127}
    rule4_out = {'channel': 2, 'type': 'note_on', 'note': 60, 'velocity': 127}
    test_tab['router'].add_rule(rule4_in, rule4_out)

    test_tab['view'].frames['list'].update_list(test_tab['router'].rules)

    # test_tab['view'].display_rules_list()
    test_tab['view'].display_rule_form()

    # active midi learn
    # test_tab['view'].frames['form'].in_form.learn_btn.invoke()

    controller.start()


if __name__ == "__main__":
    main()
