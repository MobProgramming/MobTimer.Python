from tkinter import Frame


class MobFrame(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(master, **kwargs)
        self.frames = {}
