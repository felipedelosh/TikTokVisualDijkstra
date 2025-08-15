"""
FelipedelosH
2020

Visual Efect Dijkstra
"""
from controller import Controller
from controller import PaintMode
from tkinter import *
from tkinter import ttk

class Software:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, bg="black", highlightthickness=0, bd=0)
        self.controller = Controller(self.canvas)
        self.lblTitle = Label(self.canvas, text="Dijkstra's Algorithm by FelipedelosH", bg="black", fg="white")
        self.lblGraphSelector = Label(self.canvas, text="Graph: ", bg="black", fg="white")
        _textToMsM = self.controller.textMessageToDisplayTOP
        self.lblMessageTOP = Label(self.canvas, text=_textToMsM, bg="black", fg="white", font=("Segoe UI", 20, "bold"), wraplength=320, justify="center")
        self.lblMessageBOTTOM = Label(self.canvas, text="FelipedelosH", bg="black", fg="white", font=("Segoe UI", 20, "bold"), wraplength=320, justify="center")
        _graphsOptions = self.controller.loadGraphFiles()
        self.comboGraph = ttk.Combobox(self.canvas, values=_graphsOptions, state="readonly")
        self.comboGraph.current(0)
        self.btnRunDJ = Button(self.canvas, text="RUN DIJKSTRA", bg="green", fg="black", command=self._runDijkstra)
        
        self._renderWindow()

    def _renderWindow(self):
        self.window.geometry(self.controller.getWindowSize())
        self.window.resizable(0,0)
        self.window.title("Dijkstra by LOKO v1.0")
        self.canvas['height'] = self.controller.h
        self.canvas['width'] = self.controller.w
        self.canvas.place(x=0, y=0)
        self.lblTitle.place(x=self.controller.w * 0.23, y=self.controller.h*0.03)
        self.lblGraphSelector.place(x=self.controller.w * 0.09, y=self.controller.h*0.07)
        self.lblMessageTOP.place(x=self.controller.w * 0.14, y=self.controller.h*0.15)
        self.lblMessageBOTTOM.place(x=self.controller.w * 0.2, y=self.controller.h*0.75)
        self.comboGraph.place(x=self.controller.w * 0.22, y=self.controller.h*0.07, width=self.controller.h*0.28)
        self.btnRunDJ.place(x=self.controller.w * 0.758, y=self.controller.h*0.068)
        
        self.window.after(0, self._refreshWindow)
        self.window.mainloop()

    def _refreshWindow(self):
        self.lblMessageTOP['text'] = self.controller.textMessageToDisplayTOP
        self.lblMessageBOTTOM['text'] = self.controller.textMessageToDisplayBOTTOM
        self.window.after(60, self._refreshWindow)

    def _runDijkstra(self):
        self.btnRunDJ.config(state="disabled")
        _filename_graph = self.comboGraph.get()
        isLoad  = self.controller.loadGraph(_filename_graph)

        if isLoad:
            self.btnRunDJ['bg'] = "green"
        else:
            self.btnRunDJ['bg'] = "red"
            return
        
        self.controller.set_mode(PaintMode.ANIMATION_INTRO)
        isPainted = self.controller.render()

        if isPainted:
            self.btnRunDJ['bg'] = "green"
        else:
            self.btnRunDJ['bg'] = "red"
            return


s = Software()
