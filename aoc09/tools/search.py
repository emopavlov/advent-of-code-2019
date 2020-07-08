from queue import PriorityQueue

from aoc09.tools.graph import Graph
from typing import List, Tuple, Callable, Set, Any


class Target:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

    def position(self):
        return self.x, self.y

    def __repr__(self):
        return f"Target ({self.x}, {self.y}: {self.name})"

    def __hash__(self):
        return hash((self.name, self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, Target):
            return self.name == other.name and self.x == other.x and self.y == other.y
        return NotImplemented


def bfs_to_graph(
        targets: Set[Target],
        expand: Callable[[int, int], List[Tuple[int, int]]]
) -> Graph:
    target_positions = {t.position(): t for t in targets}
    target_names = {t.name for t in targets}

    graph = Graph(target_names, [])
    for target in targets:
        starting_position = target.position()
        search_front = {starting_position}
        visited = {starting_position}
        steps = 0
        paths = {}
        found = set()

        while len(search_front) > 0 and len(found) < len(target_names):
            for xy in search_front:
                if xy in target_positions:
                    name = target_positions[xy].name
                    if name not in paths:
                        paths[name] = steps
                    found.add(name)

            expanded_front = {m for pos in search_front for m in expand(*pos) if m not in visited}
            # increment and repeat
            search_front = expanded_front
            visited = visited.union(search_front)
            steps += 1

        source = target.name
        for destination, distance in paths.items():
            if destination != source:
                graph.add_node(source, destination, distance)

    return graph


def dijkstra(
        graph: Graph,
        start: Any,
        end: Any
) -> int:

    search_front = PriorityQueue()
    search_front.put((0, start))
    visited = set()

    while not search_front.empty():
        # get top of queue
        (distance, node) = search_front.get()

        # check for target
        if node == end:
            return distance

        # skip if visited
        if node in visited:
            continue
        else:
            visited.add(node)

        # expand and push in queue
        for n, d in graph.neighbours[node].items():
            search_front.put((distance + d, n))
    return -1
