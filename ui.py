import time
import tkinter
from tkinter import *
from PIL import ImageTk, Image


class UI:
    """Class to handle UI"""
    root = tkinter.Tk()

    # Required global variables for Labels:
    status_variable = StringVar(root)
    our_lat_variable = StringVar(root)
    our_long_variable = StringVar(root)
    remote_lat_variable = StringVar(root)
    remote_long_variable = StringVar(root)
    distance_variable = StringVar(root)

    # Initializing all the widgets:
    def __init__(self):
        self.root.attributes('-fullscreen', True)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.status_variable.set("-")
        self.our_lat_variable.set("-")
        self.our_long_variable.set("-")
        self.remote_lat_variable.set("-")
        self.remote_long_variable.set("-")
        self.distance_variable.set("-")

        # Demo image at graph_label:
        self.original_image = Image.open('original_graph.png')
        self.original_graph = ImageTk.PhotoImage(self.original_image)

        # College Logo at the Corner:
        self.I2IT = Image.open('I2IT.png')
        self.I2IT.thumbnail((64, 64), Image.ANTIALIAS)
        self.college_logo = ImageTk.PhotoImage(self.I2IT)

        # Initiating all Labels used in UI:
        Label(self.root, text="GeoPi Tracker", font=("Helvetica", 20), borderwidth=4, relief='solid').pack()

        Label(self.root, image=self.college_logo).place(x=0, y=0, width=64, height=64)

        Label(self.root, text="Status : ", font=("Helvetica", 10)).place(x=200, y=100, width=120, height=25)
        self.Status_label = Label(self.root, textvariable=self.status_variable, font=("Helvetica", 10),
                                  bg="white").place(x=350, y=100, width=350, height=25)

        Label(self.root, text="Our Latitude : ", font=("Helvetica", 10)).place(x=200, y=175, width=120, height=25)
        self.Self_Lat_label = Label(self.root, textvariable=self.our_lat_variable, font=("Helvetica", 10),
                                    bg="white").place(x=350, y=175, width=120, height=25)

        Label(self.root, text="Our Longitude : ", font=("Helvetica", 10)).place(x=600, y=175, width=120, height=25)
        self.Self_Long_label = Label(self.root, textvariable=self.our_long_variable, font=("Helvetica", 10),
                                     bg="white").place(x=750, y=175, width=120, height=25)

        Label(self.root, text="Remote Latitude : ", font=("Helvetica", 10)).place(x=200, y=250, width=120, height=25)
        self.Remote_Lat_label = Label(self.root, textvariable=self.remote_lat_variable, font=("Helvetica", 10),
                                      bg="white").place(x=350, y=250, width=120, height=25)

        Label(self.root, text="Remote Longitude : ", font=("Helvetica", 10)).place(x=600, y=250, width=120, height=25)
        self.Remote_Long_label = Label(self.root, textvariable=self.remote_long_variable, font=("Helvetica", 10),
                                       bg="white").place(x=750, y=250, width=120, height=25)

        Label(self.root, text="Distance : ", font=("Helvetica", 10)).place(x=900, y=250, width=120, height=25)
        self.distance_label = Label(self.root, textvariable=self.distance_variable, font=("Helvetica", 10),
                                    bg="white").place(x=1020, y=250, width=120, height=25)

        Label(self.root, text="Real-Time Graph : ", font=("Helvetica", 10)).place(x=200, y=350, width=120, height=25)
        self.graph_label = Label(self.root, image=self.original_graph, bd=4, height=550, width=900)
        self.graph_label.place(x=250, y=377)
        self.graph_label.image = self.original_graph
        self.render_generator = self.render()

    # Using root.update() method instead of root.mainloop() which is a blocking call:

    def render(self):
        while True:
            self.root.update()
            yield True

    # Setting the 'status' Label:
    def set_status(self, stat):
        self.status_variable.set(repr(stat))
        self.render_generator.__next__()

    # Setting the 'Our Location' Labels:
    def set_our_location(self, lat, long):
        self.our_lat_variable.set(lat)
        self.our_long_variable.set(long)
        self.render_generator.__next__()

    # Setting the 'Remote Location' Labels:
    def set_remote_location(self, lat, long):
        self.remote_lat_variable.set(lat)
        self.remote_long_variable.set(long)
        self.render_generator.__next__()

    # Setting the 'distance' Label:
    def set_distance(self, distance):
        self.distance_variable.set(distance)
        self.render_generator.__next__()

    # Setting the graph image:
    def set_graph(self, image):
        new_graph = Image.open(image)
        print("IMAGE : " + image)
        graph_image = ImageTk.PhotoImage(new_graph)
        self.graph_label.configure(image=graph_image)
        self.graph_label.image = graph_image
        self.render_generator.__next__()


