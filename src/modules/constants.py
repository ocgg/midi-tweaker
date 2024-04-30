# MIDO TYPES NAME TO MIDO VALUE NAME ##########################################

MIDO_TYPES = ['note_on', 'note_off', 'control_change', 'program_change',
              'pitchwheel']

MIDO_TYPE_TO_VAL1 = {
    'note_on': 'note',
    'note_off': 'note',
    'control_change': 'control',
    'pitchwheel': 'pitch',
    'program_change': 'program',
    'sysex': 'data',
}

MIDO_TYPE_TO_VAL2 = {
    'note_on': 'velocity',
    'note_off': 'velocity',
    'control_change': 'value',
}

MIDO_TYPE_TO_VALUES = {
    'note_on': ['note', 'velocity'],
    'note_off': ['note', 'velocity'],
    'control_change': ['control', 'value'],
    'pitchwheel': ['pitch'],
    'program_change': ['program'],
    'sysex': ['data'],
}

# TODO: useless?
MIDO_ATTR_RANGE = {
    'type': ['note_on', 'note_off', 'control_change', 'pitchwheel',
             'program_change'],
    'channel': range(16),
    'note': range(128),
    'control': range(128),
    'velocity': range(128),
    'value': range(128),
    'pitch': range(-8192, 8192),
    'program': range(128),
}

FORM_ATTR_RANGE = {
    'type': ['note_on', 'note_off', 'control_change', 'pitchwheel',
             'program_change'],
    'channel': range(1, 17),
    'note': range(128),
    'control': range(128),
    'velocity': range(128),
    'value': range(128),
    'pitch': range(-8192, 8192),
    'program': range(128),
}

# MIDI PORTS INPUT VALUES #####################################################

PORT_CHOICE_NONE = 'None'
PORT_CHOICE_ALL = 'All'
PORT_CHOICE_PLACEHOLDER = 'Select a MIDI port'
