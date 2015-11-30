from tkinter import *

from forms.ScreenBlockerMenu import ScreenBlockerMenu
from infrastructure.TimeOptionsManager import TimeOptionsManager

root = Tk()

time_optons_manager = TimeOptionsManager()
screen_blocker_menu = ScreenBlockerMenu(root, time_optons_manager)

root.mainloop()
