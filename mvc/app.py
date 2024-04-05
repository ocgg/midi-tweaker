from src.models.application_model import ApplicationModel
from src.views.application_view import ApplicationView
from src.controllers.application_controller import ApplicationController


def main():
    model = ApplicationModel()
    view = ApplicationView()
    controller = ApplicationController(model, view)
    controller.start()


if __name__ == "__main__":
    main()
