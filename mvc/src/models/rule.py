class Rule:
    def __init__(self, attributes, from_msg, to_msg):
        self.attributes = attributes
        self.from_msg = from_msg
        self.to_msg = to_msg

    def apply_to(self, msg):
        return all([getattr(msg, attribute) == self.from_msg[attribute]
                    for attribute in self.attributes])

    def translate(self, msg):
        print('in:', msg)
        print('rule attr:', self.attributes)
        for attribute in self.attributes:
            # TODO: manage type conversion
            if attribute == 'type':
                continue
            setattr(msg, attribute, self.to_msg[attribute])
            print(msg)
        print('out:', msg)
        return msg

    # def convert_type(self, msg, target_type):
    #     converted_msg = mido.Message(target_type)
