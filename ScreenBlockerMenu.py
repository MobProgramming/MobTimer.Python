from tkinter import *

class ScreenBlockerMenu(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=0
        self._geom='200x200+0+0'
        master.geometry(self.get_current_window_geomitry(master, pad))
        master.bind('<Escape>',self.toggle_geom)
        self.set_always_on_top(master)
        self.remove_title_bar(master)
        self.disable_resizing(master)

    def get_current_window_geomitry(self, master, pad):
        return "{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad)

    def disable_resizing(self, master):
        master.resizable(0, 0)

    def remove_title_bar(self, master):
        master.overrideredirect(1)

    def set_always_on_top(self, master):
        master.wm_attributes("-topmost", 1)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom