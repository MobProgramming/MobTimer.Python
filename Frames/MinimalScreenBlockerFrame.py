from tkinter import ttk, N, E, W


class MinimalScreenBlockerFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,
                 tips_manager,theme_manager,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.controller = controller
        self.countdown_manager = countdown_manager
        self.time_options_manager = time_options_manager
        self.mobber_manager = mobber_manager
        self.settings_manager = settings_manager
        self.build_window_content()
        self.tips_manager = tips_manager
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)

    def build_window_content(self):
        center_frame = ttk.Frame(self)
        center_frame.grid(row=0, column=0)
        center_frame.grid_columnconfigure(0, weight=0)
        center_frame.grid_columnconfigure(1, weight=0)
        center_frame.grid_columnconfigure(2, weight=1)
        center_frame.grid_columnconfigure(3, weight=0)
        center_frame.grid_columnconfigure(4, weight=0)

        row_index = 0

        title = ttk.Label(center_frame, text="Mobbing Timer", font="Helvetica 60 bold italic")
        title.grid(row=row_index, columnspan=5, padx=150, pady=10)
        row_index += 1

        self.current_mobber_label = ttk.Label(center_frame, text="", font="Helvetica 50 bold italic",
                                              style="Highlight.TLabel")
        self.current_mobber_label.grid(row=row_index, columnspan=5, padx=30, pady=10)
        row_index += 1

        self.next_mobber_label = ttk.Label(center_frame, text="", font="Helvetica 20 bold italic")
        self.next_mobber_label.grid(row=row_index, columnspan=5, padx=30, pady=10)
        row_index += 1

        start_button = ttk.Button(center_frame, text="Continue Mobbing!", style="StartButton.TButton", )
        start_button.grid(row=row_index, column=1, columnspan=3, sticky=N + E + W, padx=10, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.show_transparent_countdown_frame())
        row_index += 1

        if self.settings_manager.get_general_enable_tips():
            self.tip_text = ttk.Label(center_frame, text="", font="Helvetica 15 bold", wraplength=500)
            self.tip_text.grid(row=row_index, columnspan=3, padx=30, pady=10)
            row_index += 1

        start_button = ttk.Button(center_frame, text="Mob Setup & Time")
        start_button.grid(row=row_index, column=2, columnspan=3, sticky=N + E + W, padx=90, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.show_screen_blocker_frame())
        row_index += 1

        start_button = ttk.Button(center_frame, text="Quit Mobbing")
        start_button.grid(row=row_index, column=2, columnspan=3, sticky=N + E + W, padx=200, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.quit_and_destroy_session())
        row_index += 1

    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        self.current_mobber_label['text'] = ""
        self.next_mobber_label['text'] = ""
        for index in range(0, mobber_list.__len__()):
            name = mobber_list[index]
            if index == driver_index:
                self.current_mobber_label['text'] = "{}, time to drive!".format(name)
            if index == navigator_index:
                self.next_mobber_label['text'] = "{}, up next!".format(name)
        if self.settings_manager.get_general_enable_tips():
            self.tip_text['text'] = self.tips_manager.get_random_tip()
