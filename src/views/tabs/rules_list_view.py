import tkinter.ttk as ttk
from src.modules.constants import (
    MIDO_ATTR_TO_LABEL,
    MIDO_BYTE1_NAMES,
    MIDO_BYTE2_NAMES,
    RULES_LIST_ALL,
)


class RulesListView(ttk.Frame):
    def __init__(self, tab_view):
        super().__init__(tab_view)

        self.rules_controls = []

        # Rules container #############
        self.rules_frame = ttk.Frame(self)

        # Add Rule button #############
        self.add_rule_btn = ttk.Button(self, text='Add Rule',
                                                  style='big.TButton')
        # Note for user ###############
        note_txt = ('Note: rules apply one by one in order. One rule is '
                    'skipped if it cannot apply to the message being routed '
                    'AND to the original MIDI IN message.')
        self.note_label = ttk.Label(self, text=note_txt, wraplength=450,
                                    justify='center',
                                    style='small.TLabel')

        # LAYOUT ##########################################

        # Rules container #############
        self.rules_frame.columnconfigure(0, weight=1, uniform='rule')
        self.rules_frame.columnconfigure(2, weight=1, uniform='rule')

        # Self ########################
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.rules_frame.grid(row=0, column=0, sticky='nsew', padx=70)
        self.add_rule_btn.grid(row=1, column=0, pady=(0, 15))
        self.note_label.grid(row=2, column=0, pady=(0, 15))

    # RULES LIST ##############################################################

    def update_list(self, rules):
        # Clear list
        for widget in self.rules_frame.winfo_children():
            widget.destroy()
        self.rules_controls = []

        # Rebuild list
        for i, rule in enumerate(rules):
            rule_elts = self._build_rule(rule)

            rule_elts['in_rule'].grid(row=i*2, column=0, sticky='e')
            rule_elts['separator'].grid(row=i*2, column=1, pady=8)
            rule_elts['out_rule'].grid(row=i*2, column=2, sticky='w')

            delete_btn = ttk.Button(self.rules_frame, text='⨯',
                                    style='icon.TButton')
            delete_btn.grid(row=i*2, column=3)

            rule_controls = {'delete_btn': delete_btn}
            self.rules_controls.append(rule_controls)
            # TODO: edit rule

            hor_separator = ttk.Frame(self.rules_frame, style='light.TFrame')
            hor_separator.grid(row=i*2+1, column=0, columnspan=3, sticky='ew')

    # PRIVATE #################################################################

    def _build_rule(self, rule):
        rules_frame = self.rules_frame

        in_container = ttk.Frame(rules_frame)
        out_container = ttk.Frame(rules_frame)
        separator = ttk.Label(rules_frame, text='⮕', style='bold.gray.TLabel')

        in_elts = self._create_rule_elements(in_container, rule.in_attrs)
        out_elts = self._create_rule_elements(out_container, rule.out_attrs)

        for i, widget in enumerate(in_elts):
            widget.grid(row=0, column=i, padx=(0, 10))
        for i, widget in enumerate(out_elts):
            widget.grid(row=0, column=i, padx=(10, 0))

        return {'in_rule': in_container,
                'separator': separator,
                'out_rule': out_container}

    def _create_rule_elements(self, frame, attrs):
        if not attrs:
            label = ttk.Label(frame, text=RULES_LIST_ALL, style='bold.TLabel')
            return [label]

        has_channel = False
        has_type = False
        has_byte1 = False
        has_byte2 = False

        for attr in attrs:
            match attr:
                case 'channel':
                    has_channel = True
                case 'type':
                    has_type = True
                    type_name = attrs['type']
                case name if name in MIDO_BYTE1_NAMES:
                    has_byte1 = True
                    byte1_name = name
                case name if name in MIDO_BYTE2_NAMES:
                    has_byte2 = True
                    byte2_name = name

        labels_containers = []

        # Channel
        if has_channel:
            value = attrs['channel']
            container = self._create_attribute_container(frame, 'CH', value)
            labels_containers.append(container)
        # Type & val 1
        if has_type and not has_byte1:
            name = MIDO_ATTR_TO_LABEL[type_name]
            container = self._create_attribute_container(frame, name)
            labels_containers.append(container)
        elif has_type and has_byte1:
            name = MIDO_ATTR_TO_LABEL[type_name]
            value = attrs[byte1_name]
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)
        elif not has_type and has_byte1:
            name = MIDO_ATTR_TO_LABEL[byte1_name]
            value = attrs[byte1_name]
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)
        # Val 2
        if has_byte2:
            name = MIDO_ATTR_TO_LABEL[byte2_name]
            value = attrs[byte2_name]
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)

        return labels_containers

    def _create_attribute_container(self, frame, name, value=None):
        container = ttk.Frame(frame)
        wl = ttk.Label(container, text=name, style='bold.TLabel')
        wl.grid(row=0, column=0)
        if isinstance(value, range):
            value = f'{value.start}-{value.stop}'
        wv = ttk.Label(container, text=value, style='bold.gray.TLabel')
        wv.grid(row=0, column=1)
        return container
