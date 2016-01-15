import configparser
from tkinter import ttk


class ThemeManager(object):
    THEME_SETTINGS = 'THEME SETTINGS'

    def __init__(self):
        self.background_color = "#FFFFFF"
        self.button_color = "#FFFFFF"
        self.text_color = "#000000"
        self.highlight_color = "#aaaaaa"

    def set_theme(self, theme_name):
        cfg_file = "Themes/{}.cfg".format(theme_name)
        config = configparser.ConfigParser()
        config.read(cfg_file)
        theme_settings_ = config[ThemeManager.THEME_SETTINGS]
        self.background_color = theme_settings_.get('background_color')
        self.button_color = theme_settings_.get('button_color')
        self.text_color = theme_settings_.get('text_color')
        self.highlight_color = theme_settings_.get('highlight_color')

        style = ttk.Style()
        style.theme_use('default')

        style.configure('TFrame', background=self.background_color)
        style.configure('TButton',
                        background=self.button_color,
                        foreground=self.text_color)
        style.map('TButton',
                  foreground=[('disabled', self.text_color),
                              ('pressed', self.text_color),
                              ('active', self.background_color)],
                  background=[('disabled', self.button_color),
                              ('pressed', '!focus', self.button_color),
                              ('active', self.highlight_color)])

        style.configure('TLabel', background=self.background_color, foreground=self.text_color)
        style.configure('Highlight.TLabel', background=self.background_color, foreground=self.highlight_color)
        style.configure("Treeview", background=self.background_color,
                        foreground=self.text_color, fieldbackground=self.background_color, font="Helvetica 16 bold",  rowheight=30
                        )
        style.element_create("plain.field", "from", "clam")
        style.configure("StartButton.TButton",font="Helvetica 50 bold")

        style.configure("EntryStyle.TEntry",
                        foreground=self.background_color,
                        fieldbackground=self.highlight_color)
