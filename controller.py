"""
FelipedelosH
2025
"""
import os
from os import scandir
import math
import json
from enum import Enum, auto
from models.Graph import Graph
from models.Node import Node


class PaintMode(Enum):
    ANIMATION_INTRO = auto()
    DRAW = auto()
    ANIMATION_DIJKSTRA = auto()


class Controller:
    def __init__(self, canvas):
        self.path = str(os.path.dirname(os.path.abspath(__file__)))
        self.canvas = canvas
        self.graph = None
        self._graphsPaths = f"{self.path}/INPUT"
        self.w = 405
        self.h = 720
        self._node_items = {}
        self._r_final = 24
        self.mode = PaintMode.DRAW

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
        
    def set_mode(self, mode: PaintMode):
        self.mode = mode

    def render(self):
        if not self.graph:
            return False
        
        if self.mode == PaintMode.ANIMATION_INTRO:
            self.animateIntro(duration_ms=900, steps=45)
            return True
        elif self.mode == PaintMode.DRAW:
            return self.drawGraph()
        elif self.mode == PaintMode.ANIMATION_DIJKSTRA:
            # Llama aquí a tu futura animación paso a paso de Dijkstra
            # self.animateDijkstra(...)
            return True
        return False
        
    def animateIntro(self, duration_ms=900, steps=45):
        if not self.graph or not self.graph.nodes:
            return

        self.clearCanvas()
        cx, cy = self.w // 2, self.h // 2

        r0 = 2
        self._node_items = {}
        for n in self.graph.nodes:
            oid = self.canvas.create_oval(cx - r0, cy - r0, cx + r0, cy + r0,fill="blue", outline="#333333", width=2, tags=("node",))
            tid = self.canvas.create_text(cx, cy, text=n.name, fill="white", font=("Segoe UI", 12, "bold"), tags=("label",))
            self._node_items[n.name] = (oid, tid)

        def ease_out_back(t):
            c1 = 1.70158
            c3 = c1 + 1
            return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

        frame = 0

        def step():
            nonlocal frame
            p = frame / float(steps)
            ep = ease_out_back(p)

            for n in self.graph.nodes:
                x = cx + (n.x - cx) * ep
                y = cy + (n.y - cy) * ep
                r = r0 + (self._r_final - r0) * ep

                oid, tid = self._node_items[n.name]
                self.canvas.coords(oid, x - r, y - r, x + r, y + r)
                self.canvas.coords(tid, x, y)

            frame += 1
            if frame <= steps:
                self.canvas.after(int(duration_ms / steps), step)
            else:
                self.drawEdges()

        step()

    def drawEdges(self):
        if not self.graph or not self.graph.edges:
            return

        edge_color = "white"
        weight_color = "white"

        dibujadas = set()

        nodes = {n.name: n for n in self.graph.nodes}

        for a_name, vecinos in self.graph.edges.items():
            a = nodes.get(a_name)
            if a is None:
                continue

            for b_name, w in vecinos:
                key = frozenset((a_name, b_name))
                if key in dibujadas:
                    continue

                b = nodes.get(b_name)
                if b is None:
                    continue

                self.canvas.create_line(a.x, a.y, b.x, b.y, fill=edge_color, width=2, tags=("edge",))

                mx, my = (a.x + b.x) / 2.0, (a.y + b.y) / 2.0
                dx, dy = b.x - a.x, b.y - a.y
                longi = math.hypot(dx, dy) or 1.0
                off = 10
                px, py = -dy / longi * off, dx / longi * off
                self.canvas.create_text(mx + px, my + py, text=str(int(w)), fill=weight_color, font=("Segoe UI", 10, "bold"), tags=("weight",))

                dibujadas.add(key)
        

    def drawGraph(self):
        """
        Draw NAME(x, y)
        """
        if self.graph:
            # DRAW CONECTIONS AND LABELS
            edge_color = "white"
            weight_color = "white"
            _control_not_draw_duplicate_edges = []
            for a_name, vecinos in self.graph.edges.items():
                a = self.graph.getNodeByName(a_name)

                for b_name, w in vecinos:
                    b = self.graph.getNodeByName(b_name)
                    w = int(w)

                    # No DRAW round trip
                    _control = f"{a_name}:{b_name}:{w}"
                    if _control not in _control_not_draw_duplicate_edges:
                        _control_not_draw_duplicate_edges.append(_control)

                    if f"{b_name}:{a_name}:{w}" in _control_not_draw_duplicate_edges:
                        continue

                    self.canvas.create_line(a.x, a.y, b.x, b.y, fill=edge_color, width=2)
                    mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
                    dx, dy = b.x - a.x, b.y - a.y
                    long = math.hypot(dx, dy) or 1
                    off = 10
                    px, py = -dy / long * off, dx / long * off
                    self.canvas.create_text(mx + px, my + py, text=str(w), fill=weight_color, font=("Segoe UI", 10, "bold"))


            # DRAW NODES
            r = 24
            node_fill_color = "blue"
            node_outline_color = "#333333"
            node_name_text_color = "white"
            for i in self.graph.nodes:
                _name = i.name
                _x = i.x
                _y = i.y
                x0, y0, x1, y1 = _x - r, _y - r, _x + r, _y + r
                self.canvas.create_oval(x0, y0, x1, y1, fill=node_fill_color, outline=node_outline_color, width=2)
                self.canvas.create_text(_x, _y, text=_name, fill=node_name_text_color, font=("Segoe UI", 12, "bold"))

            return True
        
        return False

    def clearCanvas(self):
        self.canvas.delete("all")
