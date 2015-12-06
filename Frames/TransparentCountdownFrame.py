from tkinter import *


class TransparentCountdownFrame(Frame):
    def __init__(self, parent, controller, time_options_manager, mobber_manager, countdown_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.master = parent
        self.controller = controller
        self.create_frame_content()
        countdown_manager.subscribe_to_time_changes(self.update_time_change_callback)

    def update_time_change_callback(self, days, minutes, seconds):
        if days< 0 or minutes < 0 or seconds < 0:
            self.controller.show_screen_blocker_frame()
        self.label_minutes['text'] = "{0:0>2}".format(minutes)
        self.label_seconds['text'] = "{0:0>2}".format(seconds)

    def create_frame_content(self):
        row_index = 0
        self.label_minutes = Label(self, text="10", font="Helvetica 120 bold")
        self.label_minutes.grid(row=row_index, column=0, sticky=E)
        label_colon = Label(self, text=":", font="Helvetica 120 bold")
        label_colon.grid(row=row_index, column=1, sticky=N)
        self.label_seconds = Label(self, text="30", font="Helvetica 120 bold")
        self.label_seconds.grid(row=row_index, column=2, sticky=W)
        row_index += 1