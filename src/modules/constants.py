# MIDO VALUES HANDLING ########################################################

# MIDO ATTRIBUTES NAMES ###############

MIDO_TYPES = [
    'note_on',
    'note_off',
    'control_change',
    'pitchwheel',
    'program_change',
]

MIDO_BYTE1_NAMES = ['note', 'control', 'pitch', 'program', 'data']

MIDO_BYTE2_NAMES = ['velocity', 'value']

MIDO_TYPE_TO_BYTES_NAMES = {
    'note_on': {
        'byte1': 'note',
        'byte2': 'velocity'
    },
    'note_off': {
        'byte1': 'note',
        'byte2': 'velocity'
    },
    'control_change': {
        'byte1': 'control',
        'byte2': 'value'
    },
    'pitchwheel': {'byte1': 'pitch'},
    'program_change': {'byte1': 'program'},
    'sysex': {'byte1': 'data'},
}

# MIDO ATTRIBUTES RANGES ##############

MIDO_ATTR_RANGE = {
    'type': MIDO_TYPES,
    'channel': range(16),
    'note': range(128),
    'control': range(128),
    'velocity': range(128),
    'value': range(128),
    'pitch': range(-8192, 8192),
    'program': range(128),
}

# FORM MANAGEMENT #####################

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

# VIEW  #######################################################################

# MIDO ATTRIBUTES TO TEXT #############

MIDO_ATTR_TO_LABEL = {
    'type': 'TYPE',
    'channel': 'CH',
    # Types
    'note_on': 'NOTEON',
    'note_off': 'NOTEOFF',
    'control_change': 'CC',
    'pitchwheel': 'PITCH',
    'program_change': 'PROGRAM',
    # Byte 1
    'note': 'NOTE',
    'control': 'CC',
    'pitch': 'PITCH',
    'program': 'PROGRAM',
    # Byte 2
    'velocity': 'velo',
    'value': 'val',
}

# MIDI PORTS INPUT VALUES #############

PORT_CHOICE_NONE = 'None'
PORT_CHOICE_ALL = 'All'
PORT_CHOICE_PLACEHOLDER = 'Select a MIDI port'
