"""
FelipedelosH
2025
"""
import os
from os import scandir
import json
from models.Graph import Graph
from models.Node import Node

class Controller:
    def __init__(self, canvas):
        self.path = str(os.path.dirname(os.path.abspath(__file__)))
        self.canvas = canvas
        self.graph = None
        self._graphsPaths = f"{self.path}/INPUT"
        self.w = 405
        self.h = 720

    def getWindowSize(self):
        return f"{self.w}x{self.h}"
    
    def loadGraphFiles(self):
        _filesNames = []

        try:
            for i in scandir(self._graphsPaths):
                if i.is_file():
                    if ".json" in i.name:
                        _filesNames.append(i.name)
        except:
            pass

        return _filesNames
    
    def loadGraph(self, filename):
        """
        Enter a filename example:graph.json and charge.
        """
        file_path = os.path.join(self._graphsPaths, filename)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            self.graph = Graph()
            for n in data.get("nodes", []):
                node_obj = Node(n["name"], n["x"], n["y"])
                self.graph.addNode(node_obj)

            for e in data.get("edges", []):
                self.graph.addEdge(e["from"], e["to"], e["weight"])

            return True
        except:
            return False

