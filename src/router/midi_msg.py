import mido


class MidiMsg(mido.Message):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return f"Channel:{self.channel} Type:{self.type} Note:{self.note} Velocity:{self.velocity} Control:{self.control} Value:{self.value}"


# class MidiMsg:
#     def __init__(self, msg):
#         self.raw_full = msg
#         self.raw = msg[0]
#         self.mido = mido.parse(msg)

        # self.raw_full = msg
        # self.raw = msg[0]
        # self.channel = self.raw[0] & 0xF     # lower 4 bits
        # self.msg_type = self._get_msg_type()

    # def _get_msg_type(self):
    #     # Standard MIDI message types
    #     MIDI_MSG_TYPES = {
    #         0x80: "Note Off",
    #         0x90: "Note On",
    #         0xA0: "Aftertouch",
    #         0xB0: "Control Change",
    #         0xC0: "Program Change",
    #         0xD0: "Channel Pressure",
    #         0xE0: "Pitch Bend",
    #         0xF0: "System Exclusive",
    #         0xF1: "MIDI Time Code Quarter Frame",
    #         0xF2: "Song Position Pointer",
    #         0xF3: "Song Select",
    #         0xF6: "Tune Request",
    #         0xF7: "End of Exclusive",
    #         0xF8: "Timing Clock",
    #         0xFA: "Start",
    #         0xFB: "Continue",
    #         0xFC: "Stop",
    #         0xFD: "Active Sensing",
    #         0xFE: "System Reset",
    #     }
    #     message_type_byte = self.raw[0]
    #     # Vérifier si le message est un message système ou un message de canal
    #     if message_type_byte & 0xF0 == 0xF0:
    #         # Message système
    #         return MIDI_MSG_TYPES.get(message_type_byte, "Unknown System Message")
    #     else:
    #         # Message de canal
    #         return MIDI_MSG_TYPES.get(message_type_byte & 0xF0, "Unknown Channel Message")
