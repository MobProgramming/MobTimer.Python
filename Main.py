from tkinter import *

from Infrastructure.MobberManager import MobberManager
from forms.ScreenBlockerMenu import ScreenBlockerMenu
from Infrastructure.TimeOptionsManager import TimeOptionsManager

root = Tk()

time_options_manager = TimeOptionsManager()
mobber_manager = MobberManager()
screen_blocker_menu = ScreenBlockerMenu(root, time_options_manager, mobber_manager)

root.mainloop()
