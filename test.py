from src.models.application_model import ApplicationModel
from src.views.application_view import ApplicationView
from src.controllers.application_controller import ApplicationController

import mido


def main():
    model = ApplicationModel()
    view = ApplicationView()
    controller = ApplicationController(model, view)

    first_port = mido.get_input_names()[0]
    controller.menu_controller._open_tab(first_port)
    controller.tab_controller.tabs[first_port]['view'].display_rule_form()

    controller.start()


if __name__ == "__main__":
    main()
