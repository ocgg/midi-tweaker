import tkinter.ttk as ttk


class RulesListView(ttk.Frame):
    def __init__(self, tab_view):
        super().__init__(tab_view)

        self.widgets = {}

        # Rules container
        self.rules_frame = ttk.Frame(self)

        # Add Rule button
        self.add_rule_btn = ttk.Button(self, text='Add Rule',
                                                  style='big.TButton')
        # Note for user
        note_txt = ('Note: rules apply one by one in order. One rule is '
                    'skipped if it cannot apply to the message being routed '
                    'AND to the original MIDI IN message.')
        self.note_label = ttk.Label(self, text=note_txt, wraplength=450,
                                    justify='center',
                                    style='small.TLabel')

        # LAYOUT ######################
        self.rules_frame.columnconfigure(0, weight=1, uniform='rule')
        self.rules_frame.columnconfigure(1, weight=0)
        self.rules_frame.columnconfigure(2, weight=1, uniform='rule')

        self._packer()

    # PACKER ##################################################################

    def _packer(self):
        self.rules_frame.pack(fill='x', padx=70)
        self.note_label.pack(side='bottom')
        self.add_rule_btn.pack(side='bottom', pady=(0, 15))

    def update_list(self, rules):
        # Clear list
        self.add_rule_btn.pack_forget()
        self.note_label.pack_forget()
        self.rules_frame.pack_forget()
        for widget in self.rules_frame.winfo_children():
            widget.destroy()
        # Rebuild list
        for i, rule in enumerate(rules):
            rule_elts = self._build_rule(rule)
            rule_elts['in_rule'].grid(row=i*2, column=0, sticky='e')
            rule_elts['separator'].grid(row=i*2, column=1, pady=8)
            rule_elts['out_rule'].grid(row=i*2, column=2, sticky='w')
            between_rules = ttk.Frame(self.rules_frame, style='light.TFrame')
            between_rules.grid(row=i*2+1, column=0, columnspan=3, sticky='ew')

        self._packer()

    # PRIVATE #################################################################

    def _build_rule(self, rule):
        rules_frame = self.rules_frame

        in_container = ttk.Frame(rules_frame)
        out_container = ttk.Frame(rules_frame)
        separator = ttk.Label(rules_frame, text='⮕', style='bold.gray.TLabel')

        in_elts = self._create_rule_elements(in_container, rule.in_attrs)
        out_elts = self._create_rule_elements(out_container, rule.out_attrs)

        for i, widget in enumerate(in_elts):
            widget.pack(side='left', padx=(0, 10))
        for i, widget in enumerate(out_elts):
            widget.pack(side='left', padx=(10, 0))

        return {'in_rule': in_container,
                'separator': separator,
                'out_rule': out_container}

    def _create_rule_elements(self, frame, attrs):
        if not attrs:
            label = ttk.Label(frame, text='ALL', style='bold.TLabel')
            return [label]

        MIDI_NBRS = ['note', 'control', 'pitch']
        MIDI_VALUES = ['velocity', 'value']

        labels_containers = []
        keys = attrs.keys()
        items = attrs.items()
        has_type = 'type' in keys
        has_val1 = any([k in MIDI_NBRS for k in keys])
        has_val2 = any([k in MIDI_VALUES for k in keys])

        # Channel
        if 'channel' in keys:
            value = attrs['channel']
            container = self._create_attribute_container(frame, 'CH', value)
            labels_containers.append(container)
        # Type & val 1
        if has_type and not has_val1:
            name = self._change_attr_name(attrs['type'])
            container = self._create_attribute_container(frame, name)
            labels_containers.append(container)
        elif has_type and has_val1:
            name = self._change_attr_name(attrs['type'])
            value = next((v for k, v in items if k in MIDI_NBRS))
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)
        elif not has_type and has_val1:
            attr = next((k for k in keys if k in MIDI_NBRS))
            name = self._change_attr_name(attr)
            value = next((v for k, v in items if k in MIDI_NBRS))
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)
        # Val 2
        if has_val2:
            attr = next((k for k in keys if k in MIDI_VALUES))
            name = self._change_attr_name(attr)
            value = next((v for k, v in items if k in MIDI_VALUES))
            container = self._create_attribute_container(frame, name, value)
            labels_containers.append(container)

        return labels_containers

    def _create_attribute_container(self, frame, name, value=None):
        container = ttk.Frame(frame)
        wl = ttk.Label(container, text=name, style='bold.TLabel')
        wl.pack(side='left')
        if value:
            wv = ttk.Label(container, text=value, style='bold.gray.TLabel')
            wv.pack(side='left')
        return container

    def _change_attr_name(self, attr_name):
        match attr_name:
            # Types
            case 'note_on':
                return 'NOTEON'
            case 'note_off':
                return 'NOTEOFF'
            case 'control_change':
                return 'CC'
            case 'pitchwheel':
                return 'PITCH'
            # Val 1
            case 'note':
                return 'NOTE'
            case 'control':
                return 'CC'
            case 'pitch':
                return 'pitch'
            # Val 2
            case 'velocity':
                return 'velo'
            case 'value':
                return 'val'
            # Not handled yet case
            case _:
                return attr_name.upper()
