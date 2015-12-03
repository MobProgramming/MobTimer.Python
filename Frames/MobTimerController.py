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

        self.show_frame(ScreenBlockerFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def show_screen_blocker_frame(self):
        self.show_frame(ScreenBlockerFrame)

    def show_transparent_countdown_frame(self):
        self.show_frame(TransparentCountdownFrame)
