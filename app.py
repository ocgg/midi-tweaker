from src.models.application_model import ApplicationModel
from src.views.application_view import ApplicationView
from src.controllers.application_controller import ApplicationController


def main():
    model = ApplicationModel()
    view = ApplicationView()
    controller = ApplicationController(model, view)

    # TEMPORARY #######################
    # Use it till the return of the mighty tabs functionality
    # And then delete it and show no mercy
    controller.tabs_container_controller.add_tab('Useless name')
    # /TEMPORARY ######################

    controller.start()


if __name__ == "__main__":
    main()
