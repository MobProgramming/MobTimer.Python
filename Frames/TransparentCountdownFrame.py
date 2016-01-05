from tkinter import *
from tkinter import ttk

from Infrastructure.SettingsManager import SettingsManager


class TransparentCountdownFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,
                 tips_manager,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.controller = controller
        self.mobber_manager = mobber_manager
        self.settings_manager = settings_manager  # type: SettingsManager

        self.create_frame_content()
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)
        self.countdown_manager = countdown_manager
        self.countdown_manager.subscribe_to_time_changes(self.update_time_change_callback)

    def update_time_change_callback(self, days, minutes, seconds):
        if (days < 0 or minutes < 0 or seconds < 0) and not self.controller.frame_is_screen_blocking():
            self.controller.show_minimal_screen_blocker_frame()
        self.label_time['text'] = "{0:0>2}:{1:0>2}".format(minutes, seconds)

    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        mobber_count = mobber_list.__len__()
        if mobber_count > navigator_index:
            self.label_navigator['text'] = self.get_navigator_text(mobber_list[navigator_index])
        else:
            self.label_navigator['text'] = self.get_navigator_text("")
        if mobber_count > driver_index:
            self.label_driver['text'] = self.get_driver_text(mobber_list[driver_index])
        else:
            self.label_driver['text'] = self.get_driver_text("")

    def create_frame_content(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(4, weight=1)

        row_index = 0
        count_down_timer_font = "Helvetica {} bold".format(
            self.settings_manager.get_transparent_window_count_down_timer_font_size())
        self.label_time = ttk.Label(self, text="10:00", font=count_down_timer_font)
        # self.label_time.grid(row=row_index, sticky=(N))
        self.label_time.pack()

        row_index += 1
        next_driver_font = "Helvetica {} bold".format(
            self.settings_manager.get_transparent_window_next_driver_font_size())
        self.label_navigator = ttk.Label(self, text=self.get_navigator_text(""), font=next_driver_font)
        # self.label_navigator.grid(row=row_index, sticky=(N))
        self.label_navigator.pack()

        row_index += 1
        driver_font = "Helvetica {} bold".format(self.settings_manager.get_transparent_window_driver_font_size())
        self.label_driver = ttk.Label(self, text=self.get_driver_text(""), font=driver_font)
        # self.label_driver.grid(row=row_index, sticky=(N))
        self.label_driver.pack()
        row_index += 1

    def get_navigator_text(self, name):
        return "Next: " + name

    def get_driver_text(self, name):
        return "Driver: " + name
