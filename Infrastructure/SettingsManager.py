import configparser


class SettingsManager(object):
    TRANSPARENT_WINDOW_SETTINGS = "TRANSPARENT WINDOW SETTINGS"
    GENERAL_SETTINGS = "GENERAL SETTINGS"
    TIMER_SETTINGS = "TIMER SETTINGS"
    CONTINUE_SCREEN_BLOCKER_SETTINGS = "CONTINUE SCREEN BLOCKER SETTINGS"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("MobTimer.cfg")
        self.window_settings_ = self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS]
        self.continue_screen_blocker_settings = self.config[SettingsManager.CONTINUE_SCREEN_BLOCKER_SETTINGS]
        self.general_settings_ = self.config[SettingsManager.GENERAL_SETTINGS]
        self.timer_settings_ = self.config[SettingsManager.TIMER_SETTINGS]

    def get_transparent_window_screen_size_percent(self):
        return self.window_settings_.getfloat("size percentage", 0.3)

    def get_transparent_window_alpha_percent(self):
        return self.window_settings_.getfloat("alpha percentage", 0.3)

    def get_continue_screen_blocker_window_alpha_percent(self):
        return self.continue_screen_blocker_settings.getfloat("alpha percentage", 0.2)

    def get_transparent_window_count_down_timer_font_size(self):
        return self.window_settings_.getint("count down timer font size", 30)

    def get_transparent_window_driver_font_size(self):
        return self.window_settings_.getint("driver font size", 10)

    def get_transparent_window_next_driver_font_size(self):
        return self.window_settings_.getint("next driver font size", 10)

    def get_general_theme(self):
        return self.general_settings_.get("theme", 'none')

    def get_general_team(self):
        return self.general_settings_.get("team", 'Chris,Tom')

    def get_general_minutes(self):
        return self.timer_settings_.getint("minutes", 10)

    def get_general_seconds(self):
        return self.timer_settings_.getint("seconds", 0)

    def get_general_enable_tips(self):
        return self.general_settings_.getboolean("enable tips", True)