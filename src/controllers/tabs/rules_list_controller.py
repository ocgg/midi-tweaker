class RulesListController:
    def __init__(self, tab_controller, view, router):
        self.tab_controller = tab_controller
        self.view = view
        self.rules = router.rules
        self._bind()

    def update_list(self):
        self.view.update_list(self.rules)
        self._bind_rules_controls()

    # BINDINGS ################################################################

    def _bind(self):
        # Add rule button
        add_rule_btn = self.view.add_rule_btn
        add_rule_btn.config(command=self.tab_controller.show_rule_form)

    def _bind_rules_controls(self):
        for i, controls in enumerate(self.view.rules_controls):
            controls['delete_btn'].config(command=lambda index=i:
                                          self._delete_rule(index))
            # TODO: edit rule

    # CALLBACKS ###############################################################

    def _delete_rule(self, index):
        self.rules.pop(index)
        self.update_list()
