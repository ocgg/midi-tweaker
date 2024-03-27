import rtmidi.midiconstants as consts

class Rule:
    def __init__(self, in_ch, in_note, out_ch, out_note):
        self.in_ch = in_ch
        self.in_note = in_note
        self.out_ch = out_ch
        self.out_note = out_note
        self.in_msg = [
            consts.NOTE_ON + self.in_ch,
            self.in_note,
            None
        ]
        self.out_msg = [
            consts.NOTE_ON + self.out_ch,
            self.out_note,
            None
        ]

    def __str__(self):
        return f"Route CH{self.in_ch}:N{self.in_note} to CH{self.out_ch}:N{self.out_note}"
