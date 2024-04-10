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

        in_elts = self._display_rule_attrs(in_container, rule.in_attrs)
        out_elts = self._display_rule_attrs(out_container, rule.out_attrs)

        for i, widget in enumerate(in_elts):
            widget.pack(side='left', padx=(0, 10))
        for i, widget in enumerate(out_elts):
            widget.pack(side='left', padx=(10, 0))

        return {'in_rule': in_container,
                'separator': separator,
                'out_rule': out_container}

    def _display_rule_attrs(self, frame, attrs):
        if not attrs:
            label = ttk.Label(frame, text='ALL', style='bold.TLabel')
            return [label]

        labels_containers = []
        keys = attrs.keys()
        items = attrs.items()
        has_type = 'type' in keys
        has_val1 = any([k in ['note', 'control', 'pitch'] for k in keys])
        has_val2 = any([k in ['velocity', 'value'] for k in keys])

        # Channel
        if 'channel' in keys:
            container = ttk.Frame(frame)
            value = attrs['channel']
            wl = ttk.Label(container, text='CH', style='bold.TLabel')
            wv = ttk.Label(container, text=value+1, style='bold.gray.TLabel')
            wl.pack(side='left')
            wv.pack(side='left')
            labels_containers.append(container)
        # Type & val 1
        if has_type and not has_val1:
            container = ttk.Frame(frame)
            type_name = self._change_attr_name(attrs['type'])
            wl = ttk.Label(container, text=type_name, style='bold.TLabel')
            wl.pack()
            labels_containers.append(container)
        elif has_type and has_val1:
            container = ttk.Frame(frame)
            name = self._change_attr_name(attrs['type'])
            val = [v for k, v in items if k in ['note', 'control', 'pitch']][0]
            wl = ttk.Label(container, text=name, style='bold.TLabel')
            wv = ttk.Label(container, text=val+1, style='bold.gray.TLabel')
            wl.pack(side='left')
            wv.pack(side='left')
            labels_containers.append(container)
        elif not has_type and has_val1:
            container = ttk.Frame(frame)
            attr = [k for k in keys if k in ['note', 'control', 'pitch']][0]
            name = self._change_attr_name(attr)
            val1 = [v for k, v in items if k in ['note', 'control', 'pitch']][0]
            wl = ttk.Label(container, text=name, style='bold.TLabel')
            wv = ttk.Label(container, text=val1+1, style='bold.gray.TLabel')
            wl.pack(side='left')
            wv.pack(side='left')
            labels_containers.append(container)
        # Val 2
        if has_val2:
            container = ttk.Frame(frame)
            attr = [k for k in keys if k in ['velocity', 'value']][0]
            name = self._change_attr_name(attr)
            val2 = [v for k, v in items if k in ['velocity', 'value']][0]
            wl = ttk.Label(container, text=name, style='bold.TLabel')
            wv = ttk.Label(container, text=val2+1, style='bold.gray.TLabel')
            wl.pack(side='left')
            wv.pack(side='left')
            labels_containers.append(container)

        return labels_containers

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
            case _:
                return attr_name.upper()
