import tkinter.ttk as ttk
import tkinter.font as tk_font


class ApplicationStyle(ttk.Style):
    def __init__(self, root):
        super().__init__(root)

        # FONTS #######################

        self.MAIN_FF = 'sans-serif'
        self._configure_fonts()

        # STYLES #######################

        # ttk styles
        ttk_styles = self._get_ttk_styles()
        for name, options in ttk_styles.items():
            self.configure(name, **options)

        # tk styles
        # This is in case of needing to change tkinter.tk styles
        # tk_styles = self._get_tk_styles()
        # for target, value in tk_styles.items():
        #     root.option_add(target, value)

    # PRIVATE #################################################################

    def _configure_fonts(self):
        # THESE COMMENTS ARE FOR REMEMBERING HOW TO CHANGE DEFAULT FONTS

        tk_default_font = tk_font.nametofont('TkDefaultFont')
        tk_default_font.configure(family=self.MAIN_FF)

        # To change all app fonts
        # # font_props = {'family': 'serif', 'size': 30, 'weight': 'bold'}
        # font_props = {'family': self.MAIN_FF}
        # all_fonts = tk_font.names()
        # for font_name in all_fonts:
        #     font = tk_font.nametofont(font_name)
        #     font.configure(**font_props)

    # def _get_tk_styles(self):
        # return {
        #     # Do not use this as it overrides all fonts except some...
        #     # hard to understand behaviors
        #     # '*font': 'serif 12 bold',
        # }

    def _get_ttk_styles(self):

        # FONT ########################

        FONT_NORMAL = {'font': (self.MAIN_FF, 10)}
        FONT_BOLD = {'font': (self.MAIN_FF, 10, 'bold')}
        FONT_BIG = {'font': (self.MAIN_FF, 13, 'bold')}
        FONT_VERY_BIG = {'font': (self.MAIN_FF, 15)}
        FONT_SMALL = {'font': (self.MAIN_FF, 8)}

        # COLORS ######################

        FG_GRAY = {'foreground': 'gray'}

        return {
            # LABELS ##################

            'TLabel': {
                **FONT_NORMAL,
            },
            'small.TLabel': {
                **FONT_SMALL,
                **FG_GRAY
            },
            'bold.TLabel': {
                **FONT_BOLD,
            },
            'big.TLabel': {
                **FONT_BIG,
            },
            "bold.gray.TLabel": {
                **FONT_BOLD,
                **FG_GRAY
            },
            'error.TLabel': {
                **FONT_SMALL,
                'foreground': 'red',
            },

            # BUTTONS #################

            'cancel.TButton': {
                'padding': (0, 10),
                **FG_GRAY,
            },
            'big.TButton': {
                'padding': (70, 10),
                **FONT_BOLD,
            },
            'refresh.TButton': {
                'padding': 0,
                **FONT_VERY_BIG,
                'width': 2,
            },

            # Learn button
            'learn.TButton': {
                **FONT_SMALL,
                **FG_GRAY,
            },
            'learning.TButton': {
                **FONT_SMALL,
                **FG_GRAY,
                'background': 'gray',
                'foreground': 'white',
            },

            # COMBOBOXES ##############

            'TCombobox': {
                'padding': (7, 2),
            },

            # SEPARATORS ##############

            'light.TFrame': {
                'height': 3,
                'background': '#b7b7b7',
            },
        }
