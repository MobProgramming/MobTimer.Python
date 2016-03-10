import configparser
import uuid
from tkinter import ttk


class UniqueScaledTheme(object):
    def __init__(self, scale, button_style_id, treeview_style_id, start_button_style_id, title_style_id, label_style_id,
                 clock_style_id, entry_style_id, ttk_entry_style_cannot_specify_a_font_bug,next_mobber_label_style_id
                                 ,current_mobber_label_style_id):
        self.current_mobber_label_style_id = current_mobber_label_style_id
        self.next_mobber_label_style_id = next_mobber_label_style_id
        self.ttk_entry_style_cannot_specify_a_font_bug = ttk_entry_style_cannot_specify_a_font_bug
        self.entry_style_id = entry_style_id
        self.clock_style_id = clock_style_id
        self.label_style_id = label_style_id
        self.title_style_id = title_style_id
        self.start_button_style_id = start_button_style_id
        self.treeview_style_id = treeview_style_id
        self.button_style_id = button_style_id
        self.scale = scale


class ThemeManager(object):
    THEME_SETTINGS = 'THEME SETTINGS'

    def __init__(self):
        self.background_color = "#FFFFFF"
        self.button_color = "#FFFFFF"
        self.text_color = "#000000"
        self.highlight_color = "#aaaaaa"
        self.normal_background_flash_color = True

    def toggle_flashing_background_style(self):
        style = ttk.Style()
        style.theme_use('default')
        self.normal_background_flash_color = not self.normal_background_flash_color
        if self.normal_background_flash_color:
            style.configure('TFrame', background= self.background_color)
            style.configure('TLabel', background=self.background_color, foreground=self.text_color)
        else:
            style.configure('TFrame', background= self.highlight_color)
            style.configure('TLabel', background=self.highlight_color, foreground=self.background_color)

    def reset_flashing_background_colors_to_normal(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background= self.background_color)
        style.configure('TLabel', background=self.background_color, foreground=self.text_color)

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
                        foreground=self.text_color, fieldbackground=self.background_color)
        style.element_create("plain.field", "from", "clam")

    def get_unique_theme_for_scale(self, scale):
        window_id = uuid.uuid1().__str__()
        style = ttk.Style()
        button_style_id = "{}.TButton".format(window_id)
        style.configure(button_style_id, font="Helvetica {} bold".format(int(15 * scale)))

        treeview_style_id = "{}.Treeview".format(window_id)
        style.configure(treeview_style_id, font="Helvetica {} bold".format(int(15 * scale)), rowheight=int(30 * scale))

        start_button_style_id = "StartButton{}.TButton".format(window_id)
        style.configure(start_button_style_id, font="Helvetica {} bold".format(int(50 * scale)))

        title_style_id = "TitleLabel{}.TLabel".format(window_id)
        style.configure(title_style_id, font="Helvetica {} bold".format(int(90 * scale)))

        label_style_id = "{}.TLabel".format(window_id)
        style.configure(label_style_id, font="Helvetica {} bold".format(int(15 * scale)))

        next_mobber_label_style_id = "{}NextMobber.TLabel".format(window_id)
        style.configure(next_mobber_label_style_id, font="Helvetica {}".format(int(50 * scale)))

        current_mobber_label_style_id = "{}CurrentMobber.TLabel".format(window_id)
        style.configure(current_mobber_label_style_id, font="Helvetica {} bold italic".format(int(50 * scale)))

        clock_size = int(180 * scale)
        clock_style_id = "ClockLabel{}.TLabel".format(window_id)
        style.configure(clock_style_id, font="Helvetica {} bold".format(clock_size))

        entry_style_id = "{}.TEntry".format(window_id)
        style.configure(entry_style_id,
                        foreground=self.background_color,
                        fieldbackground=self.highlight_color)

        ttk_entry_style_cannot_specify_a_font_bug = "Helvetica {} bold".format(int(16 * scale))

        return UniqueScaledTheme(scale, button_style_id, treeview_style_id, start_button_style_id, title_style_id,
                                 label_style_id, clock_style_id, entry_style_id,
                                 ttk_entry_style_cannot_specify_a_font_bug,next_mobber_label_style_id
                                 ,current_mobber_label_style_id)
