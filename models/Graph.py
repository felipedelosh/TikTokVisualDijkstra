"""
FelipedelosH
2025
"""
from models.Node import *

class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}


    def addNode(self, x):
        if x not in self.nodes:
            self.nodes.append(x)

    
    def addEdge(self, A, B, W):
        A = self.getNodeByName(A)
        B = self.getNodeByName(B)
        W = float(W)

        if A in self.nodes and B in self.nodes and W >= 0:
            if A.name not in self.edges:
                self.edges[A.name] = []

            if B.name not in self.edges:
                self.edges[B.name] = []

            self.edges[A.name].append((B.name, W))
            self.edges[B.name].append((A.name, W))

    def getNodeByName(self, name):
        node = None

        try:
            for i in self.nodes:
                if i.name == name:
                    return i
        except:
            return node
        
        return node

    def deleteNode(self, x):
        if x in self.nodes:
            self.nodes.remove(x)

            if x in self.edges:
                del self.edges[x]

            for u, v in self.edges.items():
                for k in v:
                    if k[0] == x:
                        v.remove(k)


    def getAllNeighborsWithWeight(self, node):
        """
        return a list of tuple (node, distance)
        """
        neighbors = []

        if node in self.edges:
            for i in self.edges[node]:
                neighbors.append(i)

        return neighbors
        

    def isNeighbor(self, nodeA, nodeB):
        """
        return if A have directed conection with B
        """
        if nodeA not in self.edges or nodeB not in self.nodes:
            return False
        
        for i in self.edges[nodeA]:
            if i[0] == nodeB:
                return True
            
        return False
    

    def _getNeighborWeight(self, nodeA, nodeB):
        for i in self.edges[nodeA]:
            if i[0] == nodeB:
                return i[1]


    def DFS(self, initial_node):
        visited_nodes = []

        if initial_node in self.nodes:
            stack = [initial_node]

            while stack:
                _pivot = stack.pop()

                if _pivot not in visited_nodes:
                    visited_nodes.append(_pivot)                

                    if _pivot in self.edges:
                        for i in reversed(self.edges[_pivot]):
                            if i[0] not in stack and i[0] not in visited_nodes:
                                stack.append(i[0])

        return visited_nodes


    def BFS(self, initial_node):
        visited_nodes = []

        if initial_node in self.nodes:
            queue = [initial_node]
            
            while queue:
                _pivot = queue.pop(0)
                visited_nodes.append(_pivot)
                
                if _pivot in self.edges:
                    for i in self.edges[_pivot]:
                        if i[0] not in queue and i[0] not in visited_nodes:
                            queue.append(i[0])


        return visited_nodes
    

    def getBestRoute(self, origin, destination):
        _dijkstra_steps_info = []

        if origin != destination and origin in self.nodes and destination in self.nodes:
            _dijkstra_definitive_candidates = self._makeDijkstraAlgVersionTabulated(origin)[1]

            if origin in _dijkstra_definitive_candidates and destination in _dijkstra_definitive_candidates:
                _dijkstra_steps_info = [destination] # Put Destination in route

                _pivot = _dijkstra_definitive_candidates[destination][1] # First Step
                _dijkstra_steps_info.append(_pivot)

                _counter = 0 # Controller infinite loop
                while _pivot != origin:
                    if _counter >= len(_dijkstra_definitive_candidates):
                        return []

                    _pivot = _dijkstra_definitive_candidates[_pivot][1]
                    _dijkstra_steps_info.append(_pivot)

                    _counter = _counter + 1


        return _dijkstra_steps_info[::-1] # Reversed


    def getDijkstraTable(self, start):
        _dijkstra_table_info = []

        if start in self.edges:
            _dijkstra_table_info = self._makeDijkstraAlgVersionTabulated(start)[0]


        return _dijkstra_table_info
    

    def _makeDijkstraAlgVersionTabulated(self, start):
        """
        Enter node of graph and return [DijkstraTable, SortesPath]
        """
        dijkstra = {}
        dijkstra_definitive_candidates = {} # Save the best steps exampls {"NODOX": (weight, "NODOY")}
        total_nodes = len(self.nodes) 
        visited = []
        akumulated_distance = 0

        def _init_dijkstra_table():
            nonlocal dijkstra
            dijkstra = {i : [() for i in self.nodes] for i in self.nodes}

            nonlocal start
            dijkstra[start][0] = (0, start)

        def select_min_weight_candidate_and_mark_visited(step):
            """
            Enter a index of dijkstra table and return 
            best_distance, best_candidate, previous_candiate
            """
            nonlocal dijkstra
            nonlocal visited
            nonlocal dijkstra_definitive_candidates
            best_candidate = None
            previous_candidate = None # Contains a node of min weight
            best_distance = float('inf') # to save a min distance 
            
            for i in dijkstra:
                _data = dijkstra[i][step]

                if _data == 'X':
                    continue

                if i in visited:
                    continue

                if _data == float('inf'):
                    continue

                if _data:
                    distance, node = _data

                    if distance < best_distance:
                        best_candidate = i
                        previous_candidate = node
                        best_distance = distance


            # Fill visited
            visited.append(best_candidate)

            if not best_distance:
                dijkstra_definitive_candidates[best_candidate] = (0, previous_candidate)
            else:
                dijkstra_definitive_candidates[best_candidate] = (best_distance, previous_candidate)

            # FILL TABULATED VISISTED NODES
            nonlocal total_nodes
            try:
                # BUG: in step 0 pass to next step
                if step == 0 and best_distance == 0:
                    range_to_fill = range(step+1, total_nodes)
                else:
                    dijkstra[best_candidate][step + 1] = dijkstra[best_candidate][step]
                    range_to_fill = range(step+2, total_nodes)

                for i in range_to_fill:
                    dijkstra[best_candidate][i] = 'X'
            except:
                pass


                
            return best_distance, best_candidate, previous_candidate
        

        def fill_neighbors_distances(step, node):
            nonlocal dijkstra
            nonlocal visited
            nonlocal akumulated_distance

            for i in dijkstra:
                if not i in visited:
                    if self.isNeighbor(node, i):
                        _distance = self._getNeighborWeight(node, i) + akumulated_distance

                        if step > 0:
                            # The previous step is min weight
                            if dijkstra[i][step-1] != float('inf'):
                                if dijkstra[i][step-1][0] <= _distance:
                                    dijkstra[i][step] = dijkstra[i][step-1]
                                    continue
                            

                        dijkstra[i][step] = (_distance, node)
                    else:
                        if step > 0: 
                            # Compare if previuos node is infinite
                            if dijkstra[i][step-1] != float('inf'):
                                dijkstra[i][step] = dijkstra[i][step-1]
                                continue


                        dijkstra[i][step] = float('inf')


        # Dijkstra LOGIC
        if start in self.edges:
            # STEP 0: construct table and start point
            _init_dijkstra_table()
            best_distance, best_candidate, previous_candidate = select_min_weight_candidate_and_mark_visited(0)

            for i in range(0, total_nodes):
                fill_neighbors_distances(i, best_candidate)
                best_distance, best_candidate, previous_candidate = select_min_weight_candidate_and_mark_visited(i)
                akumulated_distance = dijkstra_definitive_candidates[best_candidate][0]

        return [dijkstra, dijkstra_definitive_candidates] 


    def __str__(self):
        txt = f"GRAPH BY CRAZY MAN\n"
        txt = txt + f"Total Nodes: {len(self.nodes)}\n"
        
        
        _nodesNames = ""
        for i in self.nodes:
            _nodesNames = _nodesNames + f"{i.name} "

        _counterConections = 0
        _conections = ""
        for i in self.edges:
            _counterConections = _counterConections + len(self.edges[i])
            _conections = _conections + f"{i}: {self.edges[i]}"
        

        txt = txt + f"Total Edges: {_counterConections}\n"
        txt = txt + f"Nodes: {_nodesNames}\n"
        txt = txt + f"Conections: {_conections}\n"

        return txt 
