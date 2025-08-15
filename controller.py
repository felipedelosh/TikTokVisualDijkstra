"""
FelipedelosH
2025
"""
import os
import time
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
        self.textMessageToDisplay = "Select a GRAPH AND press RUN to LOAD"
        self.canvas = canvas
        self.graph = None
        self._graphsPaths = f"{self.path}/INPUT"
        self.w = 405
        self.h = 720
        self._node_items = {}
        self._r_final = 24
        self.mode = PaintMode.DRAW
        self.selected_origin = None
        self.selected_destination = None


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
            self.textMessageToDisplay = ""
            self.animateIntro(duration_ms=2000, steps=45)
            return True
        elif self.mode == PaintMode.DRAW:
            self.textMessageToDisplay = "Click TO Select Origin."
            self.canvas.bind("<Button-1>", self._on_click_draw)
            return self.drawGraph()
        elif self.mode == PaintMode.ANIMATION_DIJKSTRA:
            self.animateDijkstra()
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
                self.clearCanvas()
                self.set_mode(PaintMode.DRAW)
                self.render()

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
            self._node_items = {}
            for i in self.graph.nodes:
                _name, _x, _y = i.name, i.x, i.y
                x0, y0, x1, y1 = _x - r, _y - r, _x + r, _y + r
                oid = self.canvas.create_oval(
                    x0, y0, x1, y1,
                    fill=node_fill_color, outline=node_outline_color, width=2,
                    tags=("node", f"node:{_name}")
                )
                tid = self.canvas.create_text(
                    _x, _y, text=_name, fill=node_name_text_color, font=("Segoe UI", 12, "bold"),
                    tags=("label", f"label:{_name}")
                )
                self._node_items[_name] = (oid, tid)

            return True
        
        return False
    
    def _on_click_draw(self, event):
        if self.graph:
            self.selectNodeWithClickEvent(event)

    def selectNodeWithClickEvent(self, event):
        if self.mode != PaintMode.DRAW or not self._node_items:
            return

        x, y = event.x, event.y

        hit = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        picked_name = None
        for item in hit:
            for t in self.canvas.gettags(item):
                if t.startswith("node:"):
                    picked_name = t.split(":", 1)[1]
                    break
            if picked_name:
                break

        if not picked_name:
            return 
    
        # ONLY SELECT ONE ITEM
        if not self.selected_origin:
            if self.selected_origin and self.selected_origin in self._node_items:
                prev_oid, _ = self._node_items[self.selected_origin]
                self.canvas.itemconfig(prev_oid, fill="blue", outline="#333333", width=2)

            oid, _ = self._node_items[picked_name]
            self.canvas.itemconfig(oid, fill="#ffcc00", outline="#ffa500", width=3)

            self.selected_origin = picked_name
            self.textMessageToDisplay = f"Origin: {picked_name}. Now Select Destination..."
        else:
            if self.selected_origin == picked_name:
                self.textMessageToDisplay = f"The Destination BE DIFERENT to: {picked_name}"
                return
            
            self.selected_destination = picked_name
            oid_dest, _ = self._node_items[self.selected_destination]
            self.canvas.itemconfig(oid_dest, fill="#00ccff", outline="#00a0cc", width=3)

            self.textMessageToDisplay = f"FROM: {self.selected_origin} >> TO: {self.selected_destination}"

            self.canvas.unbind("<Button-1>")

            self.canvas.after(600, lambda: (
                self.set_mode(PaintMode.ANIMATION_DIJKSTRA),
                self.animateDijkstra()
            ))

    def animateDijkstra(self):
        table = self.graph.getDijkstraTable(self.selected_origin)
        if not table:
            return

        steps = len(next(iter(table.values())))
        visited = []
        step_delay = 1200 
        blink_delay = 350

        self.canvas.delete("anim_edge")
        self.textMessageToDisplay = "Running Dijkstra…"
        time.sleep(1)
        

        def do_step(step):
            if step >= steps:
                return finish()

            best = None
            for nodo, cols in table.items():
                if nodo in visited:
                    continue
                val = cols[step]
                if isinstance(val, tuple):
                    dist, prev = val
                    if (best is None) or (dist < best[1]):
                        best = (nodo, dist, prev)

            updates = []
            for nodo, cols in table.items():
                cur = cols[step]
                prev = cols[step-1] if step > 0 else None
                if isinstance(cur, tuple) and cur != prev:
                    d, p = cur
                    updates.append((nodo, d, p))

            if best:
                pivot, dist, prev = best[0], best[1], best[2]
                self._highlight_node(pivot, fill="red", outline="purple", width=3)

                if prev and prev != pivot and prev in self._node_items:
                    _ = self._highlight_edge(prev, pivot, color="#ffcc00", width=3, tag="anim_edge")

                def blink_updates(on=True, left=2):
                    for n, _, _ in updates:
                        self._highlight_node(n,
                            fill=("#00ccff" if on else "blue"),
                            outline=("#00a0cc" if on else "#333333"),
                            width=(3 if on else 2)
                        )
                    if left > 0:
                        self.canvas.after(blink_delay, lambda: blink_updates(not on, left-1))

                blink_updates(on=True, left=2)

                visited.append(pivot)

                up_txt = ", ".join(f"{n}" for n,_,_ in updates) or "—"
                self.textMessageToDisplay = f"Step {step}: visit {pivot} (d={dist}) • updates: {up_txt}"

            self.canvas.after(step_delay, lambda: do_step(step+1))

        def finish():
            if self.selected_destination:
                path = self.graph.getBestRoute(self.selected_origin, self.selected_destination)
                if path and len(path) > 1:
                    self.canvas.delete("anim_edge")
                    for i in range(len(path)-1):
                        self._highlight_edge(path[i], path[i+1], color="#00ff66", width=5, tag="anim_edge")
                    self.textMessageToDisplay = f"Shortest path: {' → '.join(path)}"
                else:
                    self.textMessageToDisplay = "No path found."

        do_step(0)

    def _highlight_node(self, name, fill, outline, width):
        oid, _ = self._node_items.get(name, (None, None))
        if oid:
            self.canvas.itemconfig(oid, fill=fill, outline=outline, width=width)

    def _highlight_edge(self, a_name, b_name, color="#ffff00", width=4, tag="anim_edge"):
        nodes = {n.name: n for n in self.graph.nodes}
        a, b = nodes.get(a_name), nodes.get(b_name)
        if not a or not b:
            return None
        return self.canvas.create_line(a.x, a.y, b.x, b.y, fill=color, width=width, tags=(tag,))

    def clearCanvas(self):
        self.canvas.delete("all")
