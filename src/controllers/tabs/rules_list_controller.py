class RulesListController:
    def __init__(self, tab_controller, view, router):
        self.tab_controller = tab_controller
        self.view = view
        self.router = router
        self._bind()

    def update_list(self):
        self.view.update_list(self.router.rules)

    # BINDINGS ################################################################

    def _bind(self):
        # Add rule button
        add_rule_btn = self.view.add_rule_btn
        add_rule_btn.config(command=lambda:
                            self.tab_controller.show_rule_form())
