from mido import Message as mido_message


class Rule:
    def __init__(self, in_attrs, out_attrs):
        self.in_attrs = in_attrs
        self.out_attrs = out_attrs
        print(in_attrs, out_attrs)
        self.is_type_conversion = self._check_type_conversion()

    def translate(self, msg):
        # TODO: PERFORMANCE IS IMPORTANT HERE
        # benchmark this method
        if self.is_type_conversion:
            # Construct new message's first byte (type + channel)
            new_msg = mido_message(type=self.out_attrs['type'],
                                   channel=msg.channel).bytes()
            # Set other bytes (values)
            new_msg[1:] = msg.bytes()[1:]
            msg = mido_message.from_bytes(new_msg)

        for attr in self.out_attrs.keys():
            if attr == 'type':
                continue
            # TODO: works only for one value. Manage ranges
            out_value = self.out_attrs[attr][0]
            setattr(msg, attr, out_value)

        return msg

    def apply_to(self, msg):
        # Filter according to in_attrs inputs
        for key in self.in_attrs.keys():
            if hasattr(msg, key) and getattr(msg, key) == self.in_attrs[key]:
                continue
            else:
                return False
        return True

    # HELPERS #################################################################

    def _msg_is_note(self, msg):
        return 'note' in msg.type

    def _msg_is_control(self, msg):
        return msg.type == 'control_change'

    def _check_type_conversion(self):
        if 'type' in self.in_attrs and 'type' in self.out_attrs:
            return self.in_attrs['type'] != self.out_attrs['type']
        elif 'type' not in self.in_attrs and 'type' in self.out_attrs:
            # TODO: Manage this
            # Here messages have no in_attrs 'type',
            # but all out_attrs type are the same after rule application
            # !!!-> COULD BE a type conversion but not always
            # Set to True for now
            return True
        else:
            return False

    # VALIDATIONS #############################################################

    # each attr should be in right type
    # each attr should be in right range
    # out attr should not be empty
