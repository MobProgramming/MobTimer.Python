from tkinter import *


class ScreenBlockerMenu(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        pad = 0
        self._geom = '200x200+0+0'
        self.set_window_properties(master, pad)
        self.build_window_content(master)

    def set_window_properties(self, master, pad):
        master.geometry(self.get_current_window_geomitry(master, pad))
        master.bind('<Escape>', self.toggle_geometry)
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

    def toggle_geometry(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

    def build_window_content(self, master):
        center_frame = Frame()

        row_index = 0
        title = Label(center_frame, text="Mobbing Timer", font="Helvetica 40 bold italic")
        title.grid(row=row_index, columnspan=3, padx=30, pady=30, sticky=N + W + E)
        row_index += 1

        title = Label(center_frame, text="Left Click to Increase, Right Click to Decrease", font="Helvetica 16 bold")
        title.grid(row=row_index, columnspan=3, padx=30, pady=0, sticky=N)
        row_index += 1

        minutes = Label(center_frame, text="10", font="Helvetica 180 bold")
        minutes.grid(row=row_index, column=0, sticky=E)

        colon = Label(center_frame, text=":", font="Helvetica 180 bold")
        colon.grid(row=row_index, column=1, sticky=N)

        seconds = Label(center_frame, text="30", font="Helvetica 180 bold")
        seconds.grid(row=row_index, column=2, sticky=W)
        row_index += 1

        label_up_next = Label(center_frame, text="Mobber Sit At the Keyboard", font="Helvetica 50 bold")
        label_up_next.grid(row=row_index, columnspan=3, padx=30, pady=0, sticky=N)
        row_index += 1

        label_up_next = Label(center_frame, text="Next Mobber get ready!", font="Helvetica 16 bold")
        label_up_next.grid(row=row_index, columnspan=3, padx=30, pady=0, sticky=N)
        row_index += 1

        add_mobber_label = Entry(center_frame, text="Add Mobber")
        add_mobber_label.grid(row=row_index, columnspan=2, sticky=N+E+W, padx=10, pady=10)

        add_mobber_button = Button(center_frame, text="Add Mobber")
        add_mobber_button.grid(row=row_index, column=2, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        names_list = Listbox(center_frame)
        names_list.grid(row=row_index, rowspan=4, columnspan=2, column=0, padx=10, pady=10, sticky=N+E+W)

        remove_mobber_button = Button(center_frame, text="Remove Mobber")
        remove_mobber_button.grid(row=row_index, column=2, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        move_mobber_up_button = Button(center_frame, text="Move Mobber Up")
        move_mobber_up_button.grid(row=row_index, column=2, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        move_mobber_down_button = Button(center_frame, text="Move Mobber Down")
        move_mobber_down_button.grid(row=row_index, column=2, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        clear_mobbers_button = Button(center_frame, text="Clear Mobbers")
        clear_mobbers_button.grid(row=row_index, column=2, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        start_button = Button(center_frame, text="Start Mobbing!",font="Helvetica 30 bold")
        start_button.grid(row=row_index, columnspan=3, sticky=N+E+W, padx=10, pady=10)
        row_index += 1

        center_frame.pack(anchor=CENTER, pady=60)
