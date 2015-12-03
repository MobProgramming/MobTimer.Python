from tkinter import Frame, Message, Button


class TransparentCountdownFrame(Frame):
    def __init__(self, parent, controller, time_options_manager, mobber_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.master = parent
        msg = Message(self, text="hello world")
        msg.pack()

        button = Button(self, text="Dismiss", command=controller.show_screen_blocker_frame)
        button.pack()