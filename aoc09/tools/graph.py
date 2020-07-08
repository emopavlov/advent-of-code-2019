class Graph:
    def __init__(self, nodes, edges):
        self.neighbours = {}
        for n in nodes:
            self.neighbours[n] = {}

        for e in edges:
            self.add_node(e.source, e.destination, e.distance)

    def add_node(self, source, destination, distance):
        self.neighbours[source][destination] = distance

    def distance(self, source, destination):
        return self.neighbours[source][destination] if destination in self.neighbours[source] else -1

    def __repr__(self):
        return "Graph: " + self.neighbours.__repr__()


class Edge:
    def __init__(self, source, destination, distance):
        self.source = source
        self.destination = destination
        self.distance = distance
