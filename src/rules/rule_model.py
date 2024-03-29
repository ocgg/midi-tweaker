class Rule:
    def __init__(self, **kwargs):
        # How to manage filter for midi_in ?
        self.in_ch = kwargs.get('in_ch')
        self.in_note = kwargs.get('in_note')
        self.out_ch = kwargs.get('out_ch')
        self.out_note = kwargs.get('out_note')
