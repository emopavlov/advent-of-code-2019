from typing import Dict


class Graph:
    def add_node(self, source, destination, distance):
        pass

    def has_node(self, node) -> bool:
        pass

    def distance(self, source, destination) -> int:
        pass

    def neighbours(self, node) -> Dict:
        pass


class DictionaryGraph(Graph):
    def __init__(self, nodes, edges):
        self.__neighbours = {}
        for n in nodes:
            self.__neighbours[n] = {}

        for e in edges:
            self.add_node(e.source, e.destination, e.distance)

    def add_node(self, source, destination, distance):
        self.__neighbours[source][destination] = distance

    def has_node(self, node):
        return node in self.__neighbours

    def distance(self, source, destination):
        return self.__neighbours[source][destination] if destination in self.__neighbours[source] else -1

    def neighbours(self, node):
        return self.__neighbours[node]

    def __repr__(self):
        return "Graph: " + self.__neighbours.__repr__()


class Edge:
    def __init__(self, source, destination, distance):
        self.source = source
        self.destination = destination
        self.distance = distance
