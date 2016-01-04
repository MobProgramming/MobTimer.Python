from tkinter import *
from tkinter import ttk


class ScreenBlockerFrame(ttk.Frame):
    def __init__(self, master, controller, time_options_manager, mobber_manager, countdown_manager, settings_manager,tips_manager,
                 **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.controller = controller
        self.countdown_manager = countdown_manager
        self.time_options_manager = time_options_manager
        self.mobber_manager = mobber_manager
        self.settings_manager = settings_manager
        self.build_window_content()
        self.time_options_manager.subscribe_to_timechange(self.time_change_callback)
        self.mobber_manager.subscribe_to_mobber_list_change(self.mobber_list_change_callback)

    def mobber_list_change_callback(self, mobber_list, driver_index, navigator_index):
        self.current_dev['text'] = ""
        for i in self.names_list.get_children():
            self.names_list.delete(i)
        for index in range(0, mobber_list.__len__()):
            name = mobber_list[index]
            if index == driver_index:
                self.current_dev['text'] = "{} time to drive!".format(name)
                name += " <= Current"
            if index == navigator_index:
                name += " <= Next"
            self.names_list.insert('', END, text=name)

    def time_change_callback(self, time, minutes, seconds):
        self.label_minutes['text'] = "{0:0>2}".format(minutes)
        self.label_seconds['text'] = "{0:0>2}".format(seconds)

    def toggle_geometry(self, event):
        geom = self.controller.winfo_geometry()
        print(geom, self._geom)
        self.controller.geometry(self._geom)
        self._geom = geom

    def build_window_content(self):
        center_frame = ttk.Frame(self)
        center_frame.grid(row=0, column=0)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=0)
        center_frame.grid_columnconfigure(2, weight=0)
        center_frame.grid_columnconfigure(3, weight=0)
        center_frame.grid_columnconfigure(4, weight=1)

        row_index = 0
        title = ttk.Label(center_frame, text="Mobbing Timer", font="Helvetica 40 bold italic")
        title.grid(row=row_index, columnspan=5, padx=30, pady=50)
        row_index += 1

        title = ttk.Label(center_frame, text="Left Click to Increase, Right Click to Decrease",
                          font="Helvetica 16 bold")
        title.grid(row=row_index, columnspan=5, padx=30, pady=0)
        row_index += 1

        self.label_minutes = ttk.Label(center_frame, text="10", font="Helvetica 180 bold")
        self.label_minutes.grid(row=row_index, column=1, sticky=E)
        self.label_minutes.bind("<Button-1>", lambda event: self.time_options_manager.increment_minutes())
        self.label_minutes.bind("<Button-3>", lambda event: self.time_options_manager.decrement_minutes())

        label_colon = ttk.Label(center_frame, text=":", font="Helvetica 180 bold")
        label_colon.grid(row=row_index, column=2, sticky=N)

        self.label_seconds = ttk.Label(center_frame, text="30", font="Helvetica 180 bold")
        self.label_seconds.grid(row=row_index, column=3, sticky=W)
        self.label_seconds.bind("<Button-1>", lambda event: self.time_options_manager.increment_seconds())
        self.label_seconds.bind("<Button-3>", lambda event: self.time_options_manager.decrement_seconds())
        row_index += 1

        self.current_dev = ttk.Label(center_frame, text="", font="Helvetica 70 bold italic")
        self.current_dev.grid(row=row_index, columnspan=5)
        row_index += 1

        self.add_mobber_entry = ttk.Entry(center_frame, style="EntryStyle.TEntry", text="Add Mobber",
                                          font="Helvetica 16 bold")
        self.add_mobber_entry.grid(row=row_index, column=1, columnspan=2, sticky=N + E + W, padx=10, pady=10)
        self.add_mobber_entry.bind("<Return>", self.add_mobber_left_click)
        self.add_mobber_entry.bind("<Control-Return>", lambda event: self.controller.show_transparent_countdown_frame()
                                   )

        add_mobber_button = ttk.Button(center_frame, text="Add Mobber")
        add_mobber_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        add_mobber_button.bind("<Button-1>", self.add_mobber_left_click)
        row_index += 1

        self.names_list = ttk.Treeview(center_frame)
        self.names_list['show'] = 'tree'
        self.names_list.grid(row=row_index, rowspan=6, columnspan=2, column=1, padx=10, pady=10, sticky=N + E + W + S)

        remove_mobber_button = ttk.Button(center_frame, text="Remove Mobber")
        remove_mobber_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        remove_mobber_button.bind("<Button-1>", lambda event: self.mobber_manager.remove_mobber(
            int(self.names_list.index(self.names_list.selection()))))
        row_index += 1

        move_mobber_up_button = ttk.Button(center_frame, text="Move Mobber Up")
        move_mobber_up_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        move_mobber_up_button.bind("<Button-1>", self.move_mobber_up_left_click)
        row_index += 1

        move_mobber_down_button = ttk.Button(center_frame, text="Move Mobber Down")
        move_mobber_down_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        move_mobber_down_button.bind("<Button-1>", self.move_mobber_down_left_click)
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Clear Mobbers")
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.clear())
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Skip Driver")
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.switch_navigator_driver())
        row_index += 1

        clear_mobbers_button = ttk.Button(center_frame, text="Rewind Driver")
        clear_mobbers_button.grid(row=row_index, column=3, sticky=N + E + W, padx=10, pady=10)
        clear_mobbers_button.bind("<Button-1>", lambda event: self.mobber_manager.rewind_driver())
        row_index += 1

        start_button = ttk.Button(center_frame, text="Start Mobbing!", style="StartButton.TButton", )
        start_button.grid(row=row_index, column=1, columnspan=3, sticky=N + E + W, padx=10, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.show_transparent_countdown_frame())
        row_index += 1

        start_button = ttk.Button(center_frame, text="Quit Mobbing!")
        start_button.grid(row=row_index, column=1, columnspan=3, sticky=N + E + W, padx=50, pady=10)
        start_button.bind("<Button-1>", lambda event: self.controller.quit_and_destroy_session())
        row_index += 1

        center_frame.grid(row=0, column=0, sticky="nsew")

        self.focus_mobber_entry()

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
