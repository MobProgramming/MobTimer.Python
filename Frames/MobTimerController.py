from tkinter import *
from Infrastructure.MobberManager import MobberManager
from Infrastructure.TimeOptionsManager import TimeOptionsManager
from Frames.ScreenBlockerFrame import ScreenBlockerFrame
from Frames.TransparentCountdownFrame import TransparentCountdownFrame


class MobTimerController(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        time_options_manager = TimeOptionsManager()
        mobber_manager = MobberManager()

        self.frames = {}
        for F in (ScreenBlockerFrame, TransparentCountdownFrame):
            frame = F(container, self, time_options_manager, mobber_manager)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen_blocker_frame()

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def show_screen_blocker_frame(self):
        self.set_full_screen_always_on_top()
        self.show_frame(ScreenBlockerFrame)

    def show_transparent_countdown_frame(self):
        self.show_frame(TransparentCountdownFrame)
        self.set_partial_screen_transparent()

    def get_current_window_geometry(self):
        return "{0}x{1}+0+0".format(
            self.winfo_screenwidth(), self.winfo_screenheight())

    def disable_resizing(self):
        self.resizable(0, 0)

    def remove_title_bar(self):
        self.overrideredirect(1)

    def set_always_on_top(self):
        self.wm_attributes("-topmost", 1)

    def set_full_screen_always_on_top(self):
        controller = self
        controller.geometry(self.get_current_window_geometry())
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()
        top_left_screen = "+0+0"
        controller.geometry(top_left_screen)
        controller.attributes("-alpha", 1)

    def set_partial_screen_transparent(self):
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()

        controller = self

        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()

        window_width = int(screenwidth * 0.3)
        window_height = int(screenheight * 0.3)
        window_size = "{0}x{1}+0+0".format(window_width, window_height)
        bottom_left_screen = "+{}+{}".format(screenwidth - window_width,screenheight - window_height)
        controller.geometry(window_size)
        controller.geometry(bottom_left_screen)
        controller.attributes("-alpha", 0.3)
