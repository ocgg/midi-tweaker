class Rule:
    def __init__(self, in_msg, out_msg):
        self.in_msg = in_msg
        self.out_msg = out_msg
        self.attributes = list(in_msg.keys())

    def translate(self, msg):
        print('in:', msg)
        print('rule attr:', self.attributes)
        if not self._apply_to(msg):
            return msg

        print(self.out_msg.keys())
        for attribute in self.out_msg.keys():
            out_value = self.out_msg[attribute]
            setattr(msg, attribute, out_value)
        print('OUT:', msg)
        return msg

    def _apply_to(self, msg):
        # Check if self.in_msg values match with msg
        for key in self.attributes:
            # TODO: this raises an error if the key is not in msg
            # (eg 'note' in control_change)
            if getattr(msg, key) == self.in_msg[key]:
                continue
            else:
                return False
        return True
