import tkinter.ttk as ttk


class RulesListView(ttk.Frame):
    def __init__(self, tab_view):
        super().__init__(tab_view)

        self.widgets = {}

        self.widgets['rules'] = ttk.Frame(self)

        self.widgets['add_rule_btn'] = ttk.Button(self, text='Add Rule',
                                                  style='big.TButton')
        note_txt = ('Note: rules apply one by one in order. One rule is '
                    'skipped if it cannot apply to the message being routed '
                    'AND to the original MIDI IN message.')
        self.widgets['note'] = ttk.Label(self, text=note_txt, wraplength=450,
                                         justify='center',
                                         style='small.TLabel')

        self.widgets['rules'].pack(expand=True)
        self.widgets['add_rule_btn'].pack(expand=True)
        self.widgets['note'].pack(side='bottom')

    def update_list(self, rules):
        for widget in self.widgets['rules'].winfo_children():
            widget.destroy()
        self.widgets['add_rule_btn'].pack_forget()
        self.widgets['note'].pack_forget()
        for rule in rules:
            self._display_rule(rule)
        self.widgets['add_rule_btn'].pack(expand=True)
        self.widgets['note'].pack(side='bottom')

    # PRIVATE #################################################################

    def _display_rule(self, rule):
        rule_frame = ttk.Frame(self.widgets['rules'])

        in_widgets = self._display_rule_attrs(rule_frame, rule.in_attrs)
        separator = ttk.Label(rule_frame, text='➞')
        out_widgets = self._display_rule_attrs(rule_frame, rule.out_attrs)

        for i, widget in enumerate(in_widgets):
            widget.grid(row=0, column=i)
        separator.grid(row=0, column=len(in_widgets))
        for i, widget in enumerate(out_widgets):
            widget.grid(row=0, column=i+len(in_widgets)+1)

        rule_frame.pack()

    def _display_rule_attrs(self, frame, attrs):
        if not attrs:
            label = ttk.Label(frame, text='ALL', style='bold.TLabel')
            return [label]

        labels = []
        keys = attrs.keys()
        items = attrs.items()
        has_type = 'type' in keys
        has_val1 = any([k in ['note', 'control', 'pitch'] for k in keys])
        has_val2 = any([k in ['velocity', 'value'] for k in keys])

        # Channel
        if 'channel' in keys:
            value = attrs['channel']
            wl = ttk.Label(frame, text='CH', style='bold.gray.TLabel')
            wv = ttk.Label(frame, text=value+1, style='TLabel')
            labels.extend([wl, wv])
        # Type & val 1
        if has_type and not has_val1:
            type_name = self._change_attr_name(attrs['type'])
            wl = ttk.Label(frame, text=type_name, style='TLabel')
            labels.append(wl)
        elif has_type and has_val1:
            name = self._change_attr_name(attrs['type'])
            val = [v for k, v in items if k in ['note', 'control', 'pitch']][0]
            wl = ttk.Label(frame, text=name, style='bold.gray.TLabel')
            wv = ttk.Label(frame, text=val+1, style='TLabel')
            labels.extend([wl, wv])
        elif not has_type and has_val1:
            attr = [k for k in keys if k in ['note', 'control', 'pitch']][0]
            name = self._change_attr_name(attr)
            val1 = [v for k, v in items if k in ['note', 'control', 'pitch']][0]
            wl = ttk.Label(frame, text=name, style='bold.gray.TLabel')
            wv = ttk.Label(frame, text=val1+1, style='TLabel')
            labels.extend([wl, wv])
        # Val 2
        if has_val2:
            attr = [k for k in keys if k in ['velocity', 'value']][0]
            name = self._change_attr_name(attr)
            val2 = [v for k, v in items if k in ['velocity', 'value']][0]
            wl = ttk.Label(frame, text=name, style='bold.gray.TLabel')
            wv = ttk.Label(frame, text=val2+1, style='TLabel')
            labels.extend([wl, wv])

        return labels

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
