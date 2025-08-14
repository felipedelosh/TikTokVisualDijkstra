"""
FelipedelosH
2020

Visual Efect Dijkstra
"""
from controller import *
from tkinter import *

class Software:
    def __init__(self):
        self.controller = Controller()
        self.window = Tk()
        self.canvas = Canvas(self.window, bg="black", highlightthickness=0, bd=0)

        self._renderWindow()

    def _renderWindow(self):
        self.window.geometry(self.controller.getWindowSize())
        self.window.resizable(0,0)
        self.window.title("Dijkstra by LOKO v1.0")
        self.canvas['height'] = self.controller.h
        self.canvas['width'] = self.controller.w
        self.canvas.place(x=0, y=0)
        
        self.window.after(0, self._refreshWindow)
        self.window.mainloop()

    def _refreshWindow(self):
        pass
        self.window.after(60, self._refreshWindow)


s = Software()
