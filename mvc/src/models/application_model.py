from .midi_port import MidiPort
# from .rule import Rule
# from .tab_router import TabRouter


class ApplicationModel:
    def __init__(self):
        self.midi_port = MidiPort()
        # self.rule = Rule
        # self.router = TabRouter
