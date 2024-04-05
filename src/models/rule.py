class Rule:
    def __init__(self, in_msg, out_msg):
        self.in_msg = in_msg
        self.out_msg = out_msg
        self.attributes = list(in_msg.keys())

    def apply_to(self, msg):
        # Check if self.in_msg values match with msg
        for key in self.attributes:
            if getattr(msg, key) in self.in_msg[key]:
                continue
            else:
                return False
        return True

    def translate(self, msg):
        print('in:', msg)
        print('rule attr:', self.attributes)
        for attribute in self.out_msg.keys():
            out_value = self.out_msg[attribute][0]
            # if msg[attribute] == out_value:
            #     continue
            setattr(msg, attribute, out_value)
        print('OUT:', msg)
        return msg
