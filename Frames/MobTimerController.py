from tkinter import *
from Infrastructure.CountdownManager import CountdownManager
from Infrastructure.MobberManager import MobberManager
from Infrastructure.TimeOptionsManager import TimeOptionsManager
from Frames.ScreenBlockerFrame import ScreenBlockerFrame
from Frames.TransparentCountdownFrame import TransparentCountdownFrame


class MobTimerController(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)



        self.time_options_manager = TimeOptionsManager()
        self.mobber_manager = MobberManager()
        self.countdown_manager = CountdownManager(self)

        self.containers = [self, Toplevel(self)]
        self.frame_types = (ScreenBlockerFrame, TransparentCountdownFrame)
        self.frames = {}
        for frame_type in self.frame_types:
                self.frames[frame_type] = []
        for s in self.containers:
            container = Frame(s)
            container.grid(row=0, column=0, sticky=N + S + E + W)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            for frame_type in self.frame_types:
                frame_instance = frame_type(container, self, self.time_options_manager, self.mobber_manager, self.countdown_manager)
                self.frames[frame_type].append(frame_instance)
                frame_instance.grid(row=0, column=0, sticky="nsew")
        self.last_frame = None
        self.show_screen_blocker_frame()
        for frame_instance in self.frames[TransparentCountdownFrame]:
            frame_instance.bind("<Enter>", self.toggle_transparent_frame_position)
        self.transparent_frame_position = 0

    def show_frame(self, frame_class):
        switched_frames = False
        if self.last_frame != frame_class:
            for frame_instances in self.frames[frame_class]:
                    # for frame in frame_instances:
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
        for container in self.containers:
            container.geometry(self.get_current_window_geometry())
            container.geometry(top_left_screen)
            container.wait_visibility(container)
            container.attributes("-alpha", 1)

    def set_partial_screen_transparent(self):
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()
        for controller in self.containers:
            screenwidth = self.winfo_screenwidth()
            screenheight = self.winfo_screenheight()
            window_width = int(screenwidth * 0.3)
            window_height = int(screenheight * 0.3)
            window_size = "{0}x{1}+0+0".format(window_width, window_height)
            controller.geometry(window_size)
            controller.attributes("-alpha", 0.3)
        self.toggle_transparent_frame_position()

    def toggle_transparent_frame_position(self, e=None):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()

        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()

        window_width = int(screenwidth * 0.3)
        window_height = int(screenheight * 0.3)

        if self.transparent_frame_position == 0:
            self.transparent_frame_position = screenwidth - window_width
        else:
            self.transparent_frame_position = 0

        bottom_left_screen = "+{}+{}".format(self.transparent_frame_position, screenheight - window_height)
        for controller in self.containers:
            controller.geometry(bottom_left_screen)
