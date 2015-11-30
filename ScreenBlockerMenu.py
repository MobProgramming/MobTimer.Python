from tkinter import Frame, Button, LEFT


class ScreenBlockerMenu(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.print_button = Button(frame, text="Print Message", command=self.print_message)
        self.print_button.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)

    def print_message(self):
        print("Hello World")