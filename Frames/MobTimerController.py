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

    def get_current_window_geometry(self, pad):
        return "{0}x{1}+0+0".format(
            self.winfo_screenwidth() - pad, self.winfo_screenheight() - pad)

    def disable_resizing(self):
        self.resizable(0, 0)

    def remove_title_bar(self):
        self.overrideredirect(1)

    def set_always_on_top(self):
        self.wm_attributes("-topmost", 1)

    def set_full_screen_always_on_top(self):
        controller = self
        controller.geometry(self.get_current_window_geometry(0))
        # controller.bind('<Escape>', self.toggle_geometry)
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()

    def set_partial_screen_transparent(self):
        geometry = '200x200+0+0'
        controller = self
        controller.geometry(geometry)
        # controller.bind('<Escape>', self.toggle_geometry)
        self.set_always_on_top()
        self.remove_title_bar()
        self.disable_resizing()