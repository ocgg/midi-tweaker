import tkinter.ttk as ttk


class ApplicationStyle(ttk.Style):

    # FONT STYLES #############################################################

    # Family, size, weight ############
    MAIN_FONT_FAMILY = 'sans-serif'
    FONT_BOLD = {'font':    (MAIN_FONT_FAMILY, 11, 'bold')}
    FONT_BIG = {'font':     (MAIN_FONT_FAMILY, 14, 'bold')}

    # Colors ##########################
    FONT_GRAY = {'foreground': 'gray'}

    def __init__(self, root):
        super().__init__(root)

        # LABELS ######################
        self.configure('bold.TLabel',
                       **self.FONT_BOLD,)
        self.configure('bold.gray.TLabel',
                       **self.FONT_BOLD,
                       **self.FONT_GRAY,)
        self.configure('big.TLabel',
                       **self.FONT_BIG,)

        # BUTTONS #####################
        self.configure('big.TButton',
                       padding=(70, 10),
                       **self.FONT_BOLD,)
