import mido


class MidiPort:
    def all(self):
        return mido.get_input_names()
