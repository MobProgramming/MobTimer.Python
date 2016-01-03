import configparser


class SettingsManager(object):
    TRANSPARENT_WINDOW_SETTINGS = "TRANSPARENT WINDOW SETTINGS"
    GENERAL_SETTINGS = "GENERAL SETTINGS"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("MobTimer.cfg")
        # with open("MobTimer.cfg", 'w') as configfile:
        #     self.config.write(configfile)

    def get_transparent_window_screen_size_percent(self):
        return self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS].getfloat("size percentage", 0.3)

    def get_transparent_window_alpha_percent(self):
        return self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS].getfloat("alpha percentage", 0.3)

    def get_transparent_window_count_down_timer_font_size(self):
        return self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS].getint("count down timer font size", 30)

    def get_transparent_window_driver_font_size(self):
        return self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS].getint("driver font size", 10)

    def get_transparent_window_next_driver_font_size(self):
        return self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS].getint("next driver font size", 10)

    def get_general_theme(self):
        return self.config[SettingsManager.GENERAL_SETTINGS].get("theme", 'none')