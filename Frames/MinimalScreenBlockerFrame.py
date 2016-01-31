from datetime import datetime
from tkinter import ttk, N, E, W
from Infrastructure import MobberManager
from Infrastructure.ImageUtility import ImageUtility
from Infrastructure.PathUtility import PathUtility
from Infrastructure.ScreenUtility import ScreenUtility


class MinimalScreenBlockerFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,
                 tips_manager, theme_manager,
                 **kwargs):
        super().__init__(master, **kwargs)
        self.showing_extend_time_button = False
        self.master = master
        self.controller = controller
        self.countdown_manager = countdown_manager
        self.time_options_manager = time_options_manager
        self.mobber_manager = mobber_manager  # type: MobberManager
        self.settings_manager = settings_manager

        self.theme_manager = theme_manager
        self.tips_manager = tips_manager
        self.build_window_content()
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)
        if self.settings_manager.get_continue_screen_blocker_show_current_time():
            self.countdown_manager.subscribe_to_time_changes(self.update_current_time)

    def update_current_time(self, days, minutes, seconds):
        self.current_time_label["text"] = datetime.now().strftime('%Y-%m-%d     %I:%M %p')

    def build_window_content(self):

        scale = self.master.monitor.height / ScreenUtility.get_expected_height()
        unique_theme = self.theme_manager.get_unique_theme_for_scale(scale)


        center_frame = ttk.Frame(self)
        center_frame.grid()

        row_index = 0

        image_utility = ImageUtility(self.theme_manager)
        icon_size = int(75*scale)
        invisible_path = PathUtility.normalize_path('images\\invisible.png')
        self.invisible_icon = image_utility.load(invisible_path, icon_size, icon_size)
        self.fade_label = ttk.Label(center_frame, image=self.invisible_icon)
        self.fade_label.grid(row=0, column=0, sticky=(N, W))
        self.fade_label.bind("<Enter>", lambda event: self.controller.fade_app())
        self.fade_label.bind("<Leave>", lambda event: self.controller.unfade_app())

        if self.settings_manager.get_general_use_logo_image():
            self.image_utility = ImageUtility(self.theme_manager)
            image_width =int(800*scale)
            image_height = int(200*scale)
            self.background_image = self.image_utility.load(self.settings_manager.get_general_logo_image_name(), image_width,
                                                            image_height, self.settings_manager.get_general_auto_theme_logo())
            title = ttk.Label(center_frame, image=self.background_image)
        else:
            title = ttk.Label(center_frame, text="Mobbing Timer", style=unique_theme.title_style_id)
        title_padx = int(150*scale)
        pad_y = int(10*scale)
        title.grid(row=row_index, column=0, columnspan=6, padx=title_padx, pady=pad_y)
        row_index += 1


        self.keyboard_icon = image_utility.load(PathUtility.normalize_path('images\\keyboard.png'), icon_size, icon_size)
        self.keyboard_label = ttk.Label(center_frame, image=self.keyboard_icon)
        self.keyboard_label.grid(row=row_index, column=1, sticky=(N, E))

        self.current_mobber_label = ttk.Label(center_frame, text="", style=unique_theme.current_mobber_label_style_id)
        self.current_mobber_label.grid(row=row_index, column=2, columnspan=1, sticky=(N, W))
        self.current_mobber_label.bind("<Button-1>", lambda event: self.mobber_manager.switch_next_driver())

        self.minions_icon = image_utility.load(PathUtility.normalize_path('images\\minions.png'), icon_size, icon_size)
        self.minions_label = ttk.Label(center_frame, image=self.minions_icon)
        self.minions_label.grid(row=row_index, column=3, sticky=(N, E))

        self.next_mobber_label = ttk.Label(center_frame, text="", style=unique_theme.next_mobber_label_style_id)
        self.next_mobber_label.grid(row=row_index, column=4, columnspan=1, sticky=(N, W))
        row_index += 1

        start_button = ttk.Button(center_frame, text="Continue Mobbing!", style=unique_theme.start_button_style_id)
        start_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=pad_y, pady=pad_y)
        start_button.bind("<Button-1>", lambda event: self.controller.show_transparent_countdown_frame())
        row_index += 1

        if self.settings_manager.get_general_enable_tips():
            self.tip_text = ttk.Label(center_frame, text="", style=unique_theme.label_style_id, wraplength=500)
            self.tip_text.grid(row=row_index, column=1, columnspan=4, padx=int(30*scale), pady=pad_y, sticky=(N))
            row_index += 1

        if self.settings_manager.get_continue_screen_blocker_show_current_time():
            self.current_time_label = ttk.Label(center_frame, text="current time", style=unique_theme.label_style_id)
            self.current_time_label.grid(row=row_index, column=1, columnspan=4, padx=int(30*scale), pady=pad_y, sticky=(N))
            row_index += 1

        if self.settings_manager.get_timer_extension_enabled() and not self.settings_manager.get_randomize_randomize_next_driver():
            minutes = self.settings_manager.get_timer_extension_minutes()
            seconds = self.settings_manager.get_timer_extension_seconds()
            self.extend_time_button = ttk.Button(center_frame, text=self.get_extend_time_button_text(), style=unique_theme.button_style_id)
            self.extend_time_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=int(90*scale), pady=pad_y)
            self.showing_extend_time_button = True
            self.extend_time_button.bind("<Button-1>",
                                         lambda event: self.controller.rewind_and_extend(minutes, seconds))
            row_index += 1

        setup_button = ttk.Button(center_frame, text="Mob Setup & Time",style=unique_theme.button_style_id)
        setup_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=int(90*scale), pady=pad_y)
        setup_button.bind("<Button-1>", lambda event: self.controller.show_screen_blocker_frame())
        row_index += 1

        quit_button = ttk.Button(center_frame, text="Quit Mobbing",style=unique_theme.button_style_id)
        quit_button.grid(row=row_index, column=1, columnspan=4, sticky=N + E + W, padx=int(90*scale), pady=pad_y)
        quit_button.bind("<Button-1>", lambda event: self.controller.quit_and_destroy_session())
        row_index += 1

    def get_extend_time_button_text(self):
        minutes = self.settings_manager.get_timer_extension_minutes()
        seconds = self.settings_manager.get_timer_extension_seconds()
        return "Extend Time By {:0>2}:{:0>2} ({})".format(minutes, seconds,
                                                       self.controller.timer_extension_count - self.controller.extensions_used)

    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        self.current_mobber_label['text'] = ""
        self.next_mobber_label['text'] = ""
        for index in range(0, mobber_list.__len__()):
            name = mobber_list[index]
            if index == driver_index:
                self.current_mobber_label['text'] = "{} ".format(name)
            if index == navigator_index:
                self.next_mobber_label['text'] = "{}".format(name)
        if self.settings_manager.get_general_enable_tips():
            self.tip_text['text'] = self.tips_manager.get_random_tip()

    def show_extend_time_button(self):
        if self.settings_manager.get_timer_extension_enabled() and not self.settings_manager.get_randomize_randomize_next_driver():
            if self.controller.extensions_used < self.controller.timer_extension_count:
                self.extend_time_button["text"] = self.get_extend_time_button_text()
                self.extend_time_button.grid()
            else:
                self.extend_time_button.grid_remove()
