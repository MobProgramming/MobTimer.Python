import configparser


class SettingsManager(object):
    TRANSPARENT_WINDOW_SETTINGS = "TRANSPARENT WINDOW SETTINGS"
    GENERAL_SETTINGS = "GENERAL SETTINGS"
    TIMER_SETTINGS = "TIMER SETTINGS"
    CONTINUE_SCREEN_BLOCKER_SETTINGS = "CONTINUE SCREEN BLOCKER SETTINGS"
    SCREEN_BLOCKER_SETTINGS = "SCREEN BLOCKER SETTINGS"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("MobTimer.cfg")
        self.window_settings_ = self.config[SettingsManager.TRANSPARENT_WINDOW_SETTINGS]
        self.continue_screen_blocker_settings = self.config[SettingsManager.CONTINUE_SCREEN_BLOCKER_SETTINGS]
        self.screen_blocker_settings = self.config[SettingsManager.SCREEN_BLOCKER_SETTINGS]
        self.general_settings_ = self.config[SettingsManager.GENERAL_SETTINGS]
        self.timer_settings_ = self.config[SettingsManager.TIMER_SETTINGS]

    def get_transparent_window_screen_size_percent(self):
        return self.window_settings_.getfloat("size percentage", 0.3)

    def get_transparent_window_alpha_percent(self):
        return self.window_settings_.getfloat("alpha percentage", 0.3)

    def get_continue_screen_blocker_window_alpha_percent(self):
        return self.continue_screen_blocker_settings.getfloat("alpha percentage", 0.2)

    def get_continue_screen_blocker_show_current_time(self):
        return self.continue_screen_blocker_settings.getboolean("show current time", True)

    def get_screen_blocker_mouse_wheel_seconds_delta(self):
        return self.screen_blocker_settings.getint("mouse wheel seconds delta", 1)

    def get_screen_blocker_click_seconds_delta(self):
        return self.screen_blocker_settings.getint("click seconds delta", 5)

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

    def get_randomize_team(self):
        return self.general_settings_.getboolean("randomize team", 'False')

    def get_randomize_randomize_next_driver(self):
        return self.general_settings_.getboolean("randomize next driver", 'False')

    def get_general_use_logo_image(self):
        return self.general_settings_.getboolean("use logo image", 'False')

    def get_general_auto_theme_logo(self):
        return self.general_settings_.getboolean("auto theme logo", 'True')

    def get_general_logo_image_name(self):
        return self.general_settings_.get("logo image name", 'none')

    def get_timer_minutes(self):
        return self.timer_settings_.getint("minutes", 10)

    def get_timer_seconds(self):
        return self.timer_settings_.getint("seconds", 0)

    def get_timer_extension_enabled(self):
        return self.timer_settings_.getboolean("extension enabled", False)

    def get_timer_extension_minutes(self):
        return self.timer_settings_.getint("extension minutes", 0)

    def get_timer_extension_seconds(self):
        return self.timer_settings_.getint("extension seconds", 30)

    def get_timer_extension_count(self):
        return self.timer_settings_.getint("extension count", 2)

    def get_general_enable_tips(self):
        return self.general_settings_.getboolean("enable tips", True)