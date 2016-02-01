import random
import uuid
from tkinter import *
from tkinter import ttk

from Infrastructure import ScreenUtility
from Infrastructure.ImageUtility import ImageUtility

TAGNAME_CURRENT_MOBBER = 'current_mobber'


class ScreenBlockerFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,
                 tips_manager, theme_manager,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.master = master  # type : OuterFrame
        self.controller = controller
        self.theme_manager = theme_manager
        self.countdown_manager = countdown_manager
        self.time_options_manager = time_options_manager
        self.mobber_manager = mobber_manager
        self.settings_manager = settings_manager
        self.mouse_wheel_seconds_delta = self.settings_manager.get_screen_blocker_mouse_wheel_seconds_delta()
        self.click_seconds_delta = self.settings_manager.get_screen_blocker_click_seconds_delta()

        self.build_window_content()
        self.time_options_manager.subscribe_to_timechange(self.time_change_callback)
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)

    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        for i in self.names_list.get_children():
            self.names_list.delete(i)
        for index in range(0, mobber_list.__len__()):
            tags = ()
            name = mobber_list[index]
            if self.controller.settings_manager.get_dojo_enabled:
                if self.controller.dojo_manager.station_drivers.__contains__(name):
                    name += " <= {}".format(self.controller.dojo_manager.station_drivers[name])
            else:
                if index == driver_index:
                    tags = (TAGNAME_CURRENT_MOBBER)
                    name += " <= Current"
                if index == navigator_index:
                    name += " <= Next"

            self.names_list.insert('', END, text=name, tags=tags)

    def time_change_callback(self, time, minutes, seconds):
        self.label_minutes['text'] = "{0:0>2}".format(minutes)
        self.label_seconds['text'] = "{0:0>2}".format(seconds)

    def toggle_geometry(self, event):
        geom = self.controller.winfo_geometry()
        self.controller.geometry(self._geom)
        self._geom = geom

    def mouse_wheel_minutes(self, event):
        if event.delta > 0:
            self.time_options_manager.increment_minutes()
        else:
            self.time_options_manager.decrement_minutes()

    def mouse_wheel_seconds(self, event):
        if event.delta > 0:
            self.time_options_manager.increment_seconds(self.mouse_wheel_seconds_delta)
        else:
            self.time_options_manager.decrement_seconds(self.mouse_wheel_seconds_delta)

    def build_window_content(self):

        scale = self.master.monitor.height / ScreenUtility.ScreenUtility.get_expected_height()
        unique_theme = self.theme_manager.get_unique_theme_for_scale(scale)

        center_frame = ttk.Frame(self)

        center_frame.grid(row=0, column=0)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=0)
        center_frame.grid_columnconfigure(2, weight=0)
        center_frame.grid_columnconfigure(3, weight=0)
        center_frame.grid_columnconfigure(4, weight=1)

        row_index = 0

        if self.settings_manager.get_general_use_logo_image():
            self.image_utility = ImageUtility(self.theme_manager)
            background_image_width = int(800 * scale)
            background_image_height = int(200 * scale)
            self.background_image = self.image_utility.load(self.settings_manager.get_general_logo_image_name(),
                                                            background_image_width,
                                                            background_image_height,
                                                            self.settings_manager.get_general_auto_theme_logo())
            title = ttk.Label(center_frame, image=self.background_image)
        else:
            title = ttk.Label(center_frame, text="Mobbing Timer", style=unique_theme.title_style_id)
        pad_x_scaled = int(10 * scale)
        title.grid(row=row_index, columnspan=5, padx=int(30 * scale), pady=(int(70 * scale), pad_x_scaled))

        row_index += 1

        instructions = ttk.Label(center_frame, text="Left Click to Increase, Right Click to Decrease, or mouse wheel",
                                 style=unique_theme.label_style_id)
        instructions.grid(row=row_index, columnspan=5, padx=int(30 * scale), pady=pad_x_scaled)
        row_index += 1

        self.label_minutes = ttk.Label(center_frame, text="10", style=unique_theme.clock_style_id)
        self.label_minutes.grid(row=row_index, column=1, sticky=E)
        self.label_minutes.bind("<Button-1>", lambda event: self.time_options_manager.increment_minutes())
        self.label_minutes.bind("<Button-3>", lambda event: self.time_options_manager.decrement_minutes())
        self.label_minutes.bind("<MouseWheel>", self.mouse_wheel_minutes)

        label_colon = ttk.Label(center_frame, text=":", style=unique_theme.clock_style_id)
        label_colon.grid(row=row_index, column=2, sticky=N)

        self.label_seconds = ttk.Label(center_frame, text="30", style=unique_theme.clock_style_id)
        self.label_seconds.grid(row=row_index, column=3, sticky=W)
        self.label_seconds.bind("<Button-1>",
                                lambda event: self.time_options_manager.increment_seconds(self.click_seconds_delta))
        self.label_seconds.bind("<Button-3>",
                                lambda event: self.time_options_manager.decrement_seconds(self.click_seconds_delta))
        self.label_seconds.bind("<MouseWheel>", self.mouse_wheel_seconds)
        row_index += 1

        self.add_mobber_entry = ttk.Entry(center_frame, style=unique_theme.entry_style_id, font=unique_theme.ttk_entry_style_cannot_specify_a_font_bug)
        self.add_mobber_entry.grid(row=row_index, column=1, columnspan=2, sticky=N + E + W, padx=pad_x_scaled)
        self.add_mobber_entry.bind("<Return>", self.add_mobber_left_click)
        self.add_mobber_entry.bind("<Control-Return>", lambda event: self.controller.show_transparent_countdown_frame())

        button_pad = (int(15 * scale), 0)

        add_mobber_button = ttk.Button(center_frame, text="Add Mobber", style=unique_theme.button_style_id)
        add_mobber_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=0)
        add_mobber_button.bind("<Button-1>", self.add_mobber_left_click)
        row_index += 1

        self.names_list = ttk.Treeview(center_frame, style=unique_theme.treeview_style_id)
        self.names_list.tag_configure(TAGNAME_CURRENT_MOBBER, background=self.theme_manager.highlight_color,
                                      foreground=self.theme_manager.background_color)
        self.names_list['show'] = 'tree'
        self.names_list.grid(row=row_index, rowspan=7, columnspan=2, column=1, padx=pad_x_scaled, pady=button_pad,
                             sticky=N + E + W + S)

        remove_mobber_button = ttk.Button(center_frame, text="Remove Mobber", style=unique_theme.button_style_id)
        remove_mobber_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        remove_mobber_button.bind("<Button-1>", lambda event: self.mobber_manager.remove_mobber(
            int(self.names_list.index(self.names_list.selection()))))
        self.names_list.bind("<Delete>", self.remove_mobber_if_screen_blocking)
        row_index += 1

        move_mobber_up_button = ttk.Button(center_frame, text="Move Mobber Up", style=unique_theme.button_style_id)
        move_mobber_up_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        move_mobber_up_button.bind("<Button-1>", self.move_mobber_up_left_click)
        row_index += 1

        move_mobber_down_button = ttk.Button(center_frame, text="Move Mobber Down", style=unique_theme.button_style_id)
        move_mobber_down_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        move_mobber_down_button.bind("<Button-1>", self.move_mobber_down_left_click)
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Clear Mobbers", style=unique_theme.button_style_id)
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.clear())
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Skip Driver", style=unique_theme.button_style_id)
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.switch_next_driver())
        row_index += 1

        if not self.settings_manager.get_randomize_randomize_next_driver():
            clear_mobbers_button = ttk.Button(center_frame, text="Rewind Driver", style=unique_theme.button_style_id)
            clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
            clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.rewind_driver())
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Add Team", style=unique_theme.button_style_id)
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        clear_mobbers_button.bind("<Button-1>", self.add_default_team)
        row_index += 1

        start_button = ttk.Button(center_frame, text="Start Mobbing!", style=unique_theme.start_button_style_id)
        start_button.grid(row=row_index, column=1, columnspan=3, sticky=N + E + W, padx=pad_x_scaled, pady=button_pad)
        start_button.bind("<Button-1>", lambda event: self.controller.show_transparent_countdown_frame())
        row_index += 1

        start_button = ttk.Button(center_frame, text="Quit Mobbing", style=unique_theme.button_style_id)
        padx_start_button = int(50 * scale)
        start_button.grid(row=row_index, column=1, columnspan=3, sticky=N + E + W, padx=padx_start_button,
                          pady=button_pad)
        start_button.bind("<Button-1>", lambda event: self.controller.quit_and_destroy_session())
        row_index += 1

        center_frame.grid(row=0, column=0, sticky="nsew")

        self.focus_mobber_entry()

    def remove_mobber_if_screen_blocking(self, event):
        if self.controller.last_frame == ScreenBlockerFrame:
            self.mobber_manager.remove_mobber(int(self.names_list.index(self.names_list.selection())))

    def add_default_team(self, event):
        team = self.settings_manager.get_general_team().split(',')
        randomize_team = self.settings_manager.get_randomize_team()
        self.mobber_manager.clear()
        if randomize_team:
            random.shuffle(team)
        for member in team:
            self.mobber_manager.add_mobber(member)

    def focus_mobber_entry(self):
        self.add_mobber_entry.focus_set()

    def move_mobber_down_left_click(self, event):
        selected_items = self.names_list.selection()
        selected_index = int(int(self.names_list.index(selected_items)))
        self.mobber_manager.move_mobber_down(selected_index)
        self.names_list.selection_set(
            self.names_list.get_children()[(selected_index + 1) % self.mobber_manager.mobber_count()])

    def move_mobber_up_left_click(self, event):
        selected_index = int(int(self.names_list.index(self.names_list.selection())))
        self.mobber_manager.move_mobber_up(selected_index)
        count = self.mobber_manager.mobber_count()
        self.names_list.selection_set(self.names_list.get_children()[((count + selected_index - 1) % count)])

    def add_mobber_left_click(self, event):
        self.mobber_manager.add_mobber(self.add_mobber_entry.get())
        self.add_mobber_entry.delete(0, END)
