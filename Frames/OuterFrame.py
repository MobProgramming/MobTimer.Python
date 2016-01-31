from tkinter import ttk


class OuterFrame(ttk.Frame):
    def __init__(self,monitor, parent):
        super().__init__(parent)
        self.monitor = monitor