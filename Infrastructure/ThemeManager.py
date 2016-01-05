import configparser
from tkinter import ttk


class ThemeManager(object):
    THEME_SETTINGS = 'THEME SETTINGS'

    def set_theme(self, theme_name):
        cfg_file = "Themes/{}.cfg".format(theme_name)
        config = configparser.ConfigParser()
        config.read(cfg_file)
        theme_settings_ = config[ThemeManager.THEME_SETTINGS]
        background_color = theme_settings_.get('background_color')
        button_color = theme_settings_.get('button_color')
        text_color = theme_settings_.get('text_color')
        highlight_color = theme_settings_.get('highlight_color')

        style = ttk.Style()
        style.theme_use('default')

        style.configure('TFrame', background=background_color)
        style.configure('TButton',
                        background=button_color,
                        foreground=text_color)
        style.map('TButton',
                  foreground=[('disabled', text_color),
                              ('pressed', text_color),
                              ('active', background_color)],
                  background=[('disabled', button_color),
                              ('pressed', '!focus', button_color),
                              ('active', highlight_color)])

        style.configure('TLabel', background=background_color, foreground=text_color)
        style.configure('Highlight.TLabel', background=background_color, foreground=highlight_color)
        style.configure("Treeview", background=background_color,
                        foreground=text_color, fieldbackground=background_color, font="Helvetica 16 bold",  rowheight=30)
        style.element_create("plain.field", "from", "clam")
        style.configure("StartButton.TButton",font="Helvetica 50 bold")

        style.configure("EntryStyle.TEntry",
                        foreground=background_color,
                        fieldbackground=highlight_color)
