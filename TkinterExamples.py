from tkinter import *

root = Tk()


def frame_exampke():
    top_frame = Frame(root)
    top_frame.pack()
    bottom_frame = Frame(root)
    bottom_frame.pack(side=BOTTOM)
    button_add_mobber = Button(top_frame, text="Add Mobber", fg="red")
    button_remove_mobber = Button(top_frame, text="Remove Mobber", fg="blue")
    button_move_up_mobber = Button(top_frame, text="Move Mobber Up", fg="green")
    button_move_down_mobber = Button(bottom_frame, text="Add Mobber Down", fg="purple")
    button_add_mobber.pack(side=LEFT)
    button_remove_mobber.pack(side=LEFT)
    button_move_up_mobber.pack(side=LEFT)
    button_move_down_mobber.pack(side=LEFT)


# frame_exampke()

def fill_example():
    one = Label(root, text="One", bg="red", fg="white")
    one.pack()
    two = Label(root, text="Two", bg="green", fg="black")
    two.pack(fill=X)
    three = Label(root, text="Three", bg="blue", fg="white")
    three.pack(side=LEFT, fill=Y)

# fill_example()

def login_layout_example():
    label_1 = Label(root, text="Mobber Name")
    label_2 = Label(root, text="Mobber Password")
    entry_1 = Entry(root)
    entry_2 = Entry(root)
    label_1.grid(row=0, sticky=E)
    label_2.grid(row=1, sticky=E)
    entry_1.grid(row=0, column=1)
    entry_2.grid(row=1, column=1)
    c = Checkbutton(root, text="keep me logged in")
    c.grid(columnspan=2)

# login_layout_example()

def button_example():
    def print_name():
        print("hello")
    button_1 = Button(root, text="something cool", command=print_name)
    button_1.pack()


# button_example()

class SomeWindow(object):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.print_button = Button(frame, text="Print Message", command = self.print_message)
        self.print_button.pack(side=LEFT)

        self.quitButton = Button(frame, text="Quit", command=frame.quit)
        self.quitButton.pack(side=LEFT)
    def print_message(self):
        print("Hello World")

stuff = SomeWindow(root)

root.mainloop()