import atexit
import uuid
from tkinter import *
from tkinter import ttk

from screeninfo import *

from Frames.ScreenBlockerFrame import ScreenBlockerFrame
from Frames.TransparentCountdownFrame import TransparentCountdownFrame
from Infrastructure.CountdownManager import CountdownManager
from Infrastructure.MobberManager import MobberManager
from Infrastructure.SessionManager import SessionManager
from Infrastructure.SettingsManager import SettingsManager
from Infrastructure.TimeOptionsManager import TimeOptionsManager


class MobTimerController(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.settings_manager = SettingsManager()

        self.time_options_manager = TimeOptionsManager()
        self.mobber_manager = MobberManager()
        self.countdown_manager = CountdownManager(self)
        self.session_manager = SessionManager(uuid)
        atexit.register(self.session_manager.clear_sessions)
        if self.session_manager.get_active_sessions().__len__() > 0:
            self.quit_and_destroy_session()

        self.session_manager.create_session()

        self.countdown_manager.subscribe_to_time_changes(self.show_screen_blocker_when_session_interupted)

        style = ttk.Style()
        print(style.theme_names())
        theme = self.settings_manager.get_general_theme()
        if theme != "none":
            style.theme_use(theme)

        monitors = get_monitors()
        num_monitors = monitors.__len__()
        self.containers = [self]
        for monitor_index in range(1, num_monitors):
            monitor_screen_blocker = Toplevel(self)
            self.containers.append(monitor_screen_blocker)
        self.frame_types = (ScreenBlockerFrame, TransparentCountdownFrame)
        self.frames = {}
        for frame_type in self.frame_types:
            self.frames[frame_type] = []
        for container in self.containers:
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            container_frame = ttk.Frame(container)

            container_frame.grid(row=0, column=0, sticky=(N , S , E , W))
            container_frame.grid_rowconfigure(0, weight=1)
            container_frame.grid_columnconfigure(0, weight=1)
            for frame_type in self.frame_types:
                frame_instance = frame_type(container_frame, self, self.time_options_manager, self.mobber_manager,
                                            self.countdown_manager, self.settings_manager)
                self.frames[frame_type].append(frame_instance)
                frame_instance.grid(row=0, column=0, sticky=(N , S , E , W))
                frame_instance.grid_rowconfigure(0, weight=1)
                frame_instance.grid_columnconfigure(0, weight=1)
        self.last_frame = None
        self.show_screen_blocker_frame()
        for frame_instance in self.frames[TransparentCountdownFrame]:
            frame_instance.bind("<Enter>", self.toggle_transparent_frame_position)
        self.transparent_frame_position = 0
        self.title("Mob Timer")

    def quit_and_destroy_session(self):
        self.session_manager.clear_sessions()
        self.quit()
        sys.exit()

    def show_screen_blocker_when_session_interupted(self, days, minutes, seconds):
        if self.session_manager.get_active_sessions().__len__() == 0:
            self.show_screen_blocker_frame()
            self.session_manager.create_session()

    def show_frame(self, frame_class):
        switched_frames = False
        if self.last_frame != frame_class:
            for frame_instances in self.frames[frame_class]:
                frame_instances.tkraise()
            switched_frames = True
        self.last_frame = frame_class
        return switched_frames

    def show_screen_blocker_frame(self):
        if self.show_frame(ScreenBlockerFrame):
            self.mobber_manager.switch_navigator_driver()
            self.set_full_screen_always_on_top()

    def show_transparent_countdown_frame(self):
        if self.show_frame(TransparentCountdownFrame):
            self.set_partial_screen_transparent()

    def get_current_window_geometry(self):
        return "{0}x{1}+0+0".format(
            self.winfo_screenwidth(), self.winfo_screenheight())

    def disable_resizing(self):
        for container in self.containers:
            container.resizable(0, 0)

    def remove_title_bar(self):
        for container in self.containers:
            container.overrideredirect(1)

    def set_always_on_top(self):
        for container in self.containers:
            container.wm_attributes("-topmost", 1)

    def set_full_screen_always_on_top(self):
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()
        top_left_screen = "+0+0"
        monitors = get_monitors()

        for container, monitor in zip(self.containers, monitors):
            monitor_string = "{}x{}+{}+{}".format(monitor.width, monitor.height, monitor.x, monitor.y)
            container.geometry(monitor_string)
            container.wait_visibility(container)
            container.attributes("-alpha", 1)

    def set_partial_screen_transparent(self):
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()
        for controller in self.containers:
            screenwidth = self.winfo_screenwidth()
            screenheight = self.winfo_screenheight()

            size_percentage = self.settings_manager.get_transparent_window_screen_size_percent()
            alpha = self.settings_manager.get_transparent_window_alpha_percent()
            window_width = int(screenwidth * size_percentage)
            window_height = int(screenheight * size_percentage)
            window_size = "{0}x{1}+0+0".format(window_width, window_height)
            controller.geometry(window_size)
            controller.attributes("-alpha", alpha)
        self.toggle_transparent_frame_position()

    def toggle_transparent_frame_position(self, e=None):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()

        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()

        size_percentage = self.settings_manager.get_transparent_window_screen_size_percent()

        window_width = int(screenwidth * size_percentage)
        window_height = int(screenheight * size_percentage)

        if self.transparent_frame_position == 0:
            self.transparent_frame_position = screenwidth - window_width
        else:
            self.transparent_frame_position = 0

        bottom_left_screen = "+{}+{}".format(self.transparent_frame_position, screenheight - window_height)
        for controller in self.containers:
            controller.geometry(bottom_left_screen)
