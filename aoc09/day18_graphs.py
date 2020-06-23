from aoc09.util import read_input
from aoc09.tools.matrix import Matrix
from typing import Tuple, List, Set, Dict
from queue import PriorityQueue

# --- Day 18: Many-Worlds Interpretation ---
#
# As you approach Neptune, a planetary security system detects you and activates a giant tractor beam on Triton! You have no choice but to land.
#
# A scan of the local area reveals only one interesting feature: a massive underground vault. You generate a map of the tunnels (your puzzle input). The tunnels are too narrow to move diagonally.
#
# Only one entrance (marked @) is present among the open passages (marked .) and stone walls (#), but you also detect an assortment of keys (shown as lowercase letters) and doors (shown as uppercase letters). Keys of a given letter open the door of the same letter: a opens A, b opens B, and so on. You aren't sure which key you need to disable the tractor beam, so you'll need to collect all of them.
#
# For example, suppose you have the following map:
#
# #########
# #b.A.@.a#
# #########
#
# Starting from the entrance (@), you can only access a large door (A) and a key (a). Moving toward the door doesn't help you, but you can move 2 steps to collect the key, unlocking A in the process:
#
# #########
# #b.....@#
# #########
#
# Then, you can move 6 steps to collect the only other key, b:
#
# #########
# #@......#
# #########
#
# So, collecting every key took a total of 8 steps.
#
# Here is a larger example:
#
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################
#
# The only reasonable move is to take key a and unlock door A:
#
# ########################
# #f.D.E.e.C.b.....@.B.c.#
# ######################.#
# #d.....................#
# ########################
#
# Then, do the same with key b:
#
# ########################
# #f.D.E.e.C.@.........c.#
# ######################.#
# #d.....................#
# ########################
#
# ...and the same with key c:
#
# ########################
# #f.D.E.e.............@.#
# ######################.#
# #d.....................#
# ########################
#
# Now, you have a choice between keys d and e. While key e is closer, collecting it now would be slower in the long run than collecting key d first, so that's the best choice:
#
# ########################
# #f...E.e...............#
# ######################.#
# #@.....................#
# ########################
#
# Finally, collect key e to unlock door E, then collect key f, taking a grand total of 86 steps.
#
# Here are a few more examples:
#
#     ########################
#     #...............b.C.D.f#
#     #.######################
#     #.....@.a.B.c.d.A.e.F.g#
#     ########################
#
#     Shortest path is 132 steps: b, a, c, d, f, e, g
#
#     #################
#     #i.G..c...e..H.p#
#     ########.########
#     #j.A..b...f..D.o#
#     ########@########
#     #k.E..a...g..B.n#
#     ########.########
#     #l.F..d...h..C.m#
#     #################
#
#     Shortest paths are 136 steps;
#     one is: a, f, b, j, g, n, h, d, l, o, e, p, c, i, k, m
#
#     ########################
#     #@..............ac.GI.b#
#     ###d#e#f################
#     ###A#B#C################
#     ###g#h#i################
#     ########################
#
#     Shortest paths are 81 steps; one is: a, c, f, i, d, g, b, e, h
#
# How many steps is the shortest path that collects all of the keys?

# 1. Travelling salesman through all keys.
# Needs graph of distances between keys.
# There are additional constraints that some keys are only accessible after other.
# ? key order is defined by doors, e.g. to get "g" in the last example you must first get "a". There is key "rank"

WALL = "#"
OPEN = "."
START = "@"

Tile = Tuple[int, int]
Position = Tuple[int, int, str]  # x, y, passed doors


def doors(pos: Position) -> str:
    return pos[2]


def coordinates(pos: Position) -> Tuple[int, int]:
    return pos[0], pos[1]


def is_door(tile: chr) -> bool:
    return "A" <= tile <= "Z"


def is_key(tile: chr) -> bool:
    return "a" <= tile <= "z"


def all_keys(the_map: List[str]) -> Set[str]:
    return set(filter(is_key, '\n'.join(the_map)))


def map_to_matrix(the_map: List[str]) -> Matrix:
    m = Matrix()
    m.init_from_string('\n'.join(the_map))
    return m


def find_edges(the_map: Matrix, start: str, targets: Set[str]) -> Dict[str, Tuple[int, str]]:
    return find_edges_at(the_map, the_map.index_of(start), targets)


def find_edges_at(the_map: Matrix, start: Tuple[int, int], targets: Set[str]) -> Dict[str, Tuple[int, str]]:

    def legal_moves(pos: Position) -> Set[Position]:
        x, y, passed_doors = pos

        def accessible(tile):
            x, y = tile
            if 0 <= x < the_map.width and 0 <= y < the_map.height:
                tile_value = the_map.get(x, y)
                return tile_value != WALL
            else:
                return False

        moves = [
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y)
        ]
        positions = set(map(lambda x: move_to_position(x[0], x[1], passed_doors), filter(accessible, moves)))
        return positions

    def move_to_position(x, y, passed_doors):
        tile = the_map.get(x, y)
        if is_door(tile) and tile not in passed_doors:
            return x, y, ''.join(sorted(passed_doors + tile))
        else:
            return x, y, passed_doors

    # BFS
    starting_position = start + ("",)
    search_front = {starting_position}
    visited = {starting_position}
    steps = 0
    paths = {}
    found = set()

    while len(search_front) > 0 and found != targets:
        for p in search_front:
            xy = coordinates(p)
            tile = the_map.get(*xy)
            if tile in targets:
                if tile not in paths:
                    paths[tile] = (steps, doors(p))
                found.add(tile)

        expanded_front = {m for pos in search_front for m in legal_moves(pos) if m not in visited}
        # increment and repeat
        search_front = expanded_front
        visited = visited.union(search_front)
        steps += 1

    return paths


class Graph:
    def __init__(self):
        self.the_graph = {}

    def put(self, source, destination, distance, doors_passed):
        val = (distance, doors_passed)
        if source in self.the_graph and destination in self.the_graph[source]:
            if self.the_graph[source][destination] != val:
                print(f"Found alternative route for {(source, destination)}, was {self.the_graph[source][destination]}, new one is {val}")
        if source not in self.the_graph:
            self.the_graph[source] = {}  # initiate source dict
        self.the_graph[source][destination] = val

        if destination not in self.the_graph:
            self.the_graph[destination] = {}  # initiate destination dict
        self.the_graph[destination][source] = val

    def get(self, source: str) -> Dict[str, Tuple[int, str]]:
        return self.the_graph[source]

    def all_nodes(self) -> str:
        return ''.join(sorted(self.the_graph.keys()))


def map_to_graph(the_map: Matrix):
    graph = Graph()
    keys_to_collect = all_keys(the_map.values)
    paths_from_start = find_edges(the_map, "@", keys_to_collect)
    for k, v in paths_from_start.items():
        graph.put("@", k, *v)

    while len(keys_to_collect) > 0:
        key = keys_to_collect.pop()
        paths = find_edges(the_map, key, keys_to_collect)
        for k, v in paths.items():
            graph.put(key, k, *v)

    return graph


Node = str
Walker = Tuple[str, str]  # node, collected keys (ordered)
WalkerWithDoors = Tuple[Walker, Set[str]]  # walker, unlocked doors set


def expand_walker(w: WalkerWithDoors, graph: Graph) -> List[Tuple[int, WalkerWithDoors]]:  # List[(step length, new walker)]
    def new_walker(w: WalkerWithDoors, dest: Node, gates: str) -> WalkerWithDoors:
        (walker, open_doors) = w
        for g in gates:
            if g not in open_doors:
                return None
        keys = "".join(sorted(set(list(walker[1]) + [dest])))
        return (dest, keys), open_doors.union({dest.upper()})

    (walker, _) = w
    all_walkers = [(d, new_walker(w, dest, g)) for dest, (d, g) in graph.get(walker[0]).items()]
    return [r for r in all_walkers if not None == r[1]]


def walk_graph(graph: Graph, start_at: str) -> int:

    # BFS
    w0 = (start_at, start_at)
    initial_walker = (w0, set())
    search_front = PriorityQueue()
    search_front.put((0, initial_walker))
    visited = set()
    target = graph.all_nodes()

    while not search_front.empty():
        # get top of queue
        (distance, walker_with_doors) = search_front.get()

        # check for target
        (walker, open_doors) = walker_with_doors
        (_, collected_keys) = walker
        if collected_keys == target:
            return distance

        # skip if visited
        if walker in visited:
            continue
        else:
            visited.add(walker)

        # expand and push in queue
        for d, w in expand_walker(walker_with_doors, graph):
            search_front.put((distance + d, w))

    return -1


if __name__ == "__main__":
    import time
    s_time = time.time()

    m = map_to_matrix(read_input("day18"))
    g = map_to_graph(m)
    n = walk_graph(g, "@")
    print("Part One: ", n)

    print("time: ", time.time() - s_time)


# --- Part Two ---
#
# You arrive at the vault only to discover that there is not one vault, but four - each with its own entrance.
#
# On your map, find the area in the middle that looks like this:
#
# ...
# .@.
# ...
#
# Update your map to instead use the correct data:
#
# @#@
# ###
# @#@
#
# This change will split your map into four separate sections, each with its own entrance:
#
# #######       #######
# #a.#Cd#       #a.#Cd#
# ##...##       ##@#@##
# ##.@.##  -->  #######
# ##...##       ##@#@##
# #cB#Ab#       #cB#Ab#
# #######       #######
#
# Because some of the keys are for doors in other vaults, it would take much too long to collect all of the keys by yourself. Instead, you deploy four remote-controlled robots. Each starts at one of the entrances (@).
#
# Your goal is still to collect all of the keys in the fewest steps, but now, each robot has its own position and can move independently. You can only remotely control a single robot at a time. Collecting a key instantly unlocks any corresponding doors, regardless of the vault in which the key or door is found.
#
# For example, in the map above, the top-left robot first collects key a, unlocking door A in the bottom-right vault:
#
# #######
# #@.#Cd#
# ##.#@##
# #######
# ##@#@##
# #cB#.b#
# #######
#
# Then, the bottom-right robot collects key b, unlocking door B in the bottom-left vault:
#
# #######
# #@.#Cd#
# ##.#@##
# #######
# ##@#.##
# #c.#.@#
# #######
#
# Then, the bottom-left robot collects key c:
#
# #######
# #@.#.d#
# ##.#@##
# #######
# ##.#.##
# #@.#.@#
# #######
#
# Finally, the top-right robot collects key d:
#
# #######
# #@.#.@#
# ##.#.##
# #######
# ##.#.##
# #@.#.@#
# #######
#
# In this example, it only took 8 steps to collect all of the keys.
#
# Sometimes, multiple robots might have keys available, or a robot might have to wait for multiple keys to be collected:
#
# ###############
# #d.ABC.#.....a#
# ######@#@######
# ###############
# ######@#@######
# #b.....#.....c#
# ###############
#
# First, the top-right, bottom-left, and bottom-right robots take turns collecting keys a, b, and c, a total of 6 + 6 + 6 = 18 steps. Then, the top-left robot can access key d, spending another 6 steps; collecting all of the keys here takes a minimum of 24 steps.
#
# Here's a more complex example:
#
# #############
# #DcBa.#.GhKl#
# #.###@#@#I###
# #e#d#####j#k#
# ###C#@#@###J#
# #fEbA.#.FgHi#
# #############
#
#     Top-left robot collects key a.
#     Bottom-left robot collects key b.
#     Top-left robot collects key c.
#     Bottom-left robot collects key d.
#     Top-left robot collects key e.
#     Bottom-left robot collects key f.
#     Bottom-right robot collects key g.
#     Top-right robot collects key h.
#     Bottom-right robot collects key i.
#     Top-right robot collects key j.
#     Bottom-right robot collects key k.
#     Top-right robot collects key l.
#
# In the above example, the fewest steps to collect all of the keys is 32.
#
# Here's an example with more choices:
#
# #############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############
#
# One solution with the fewest steps is:
#
#     Top-left robot collects key e.
#     Top-right robot collects key h.
#     Bottom-right robot collects key i.
#     Top-left robot collects key a.
#     Top-left robot collects key b.
#     Top-right robot collects key c.
#     Top-left robot collects key d.
#     Top-left robot collects key f.
#     Top-left robot collects key g.
#     Bottom-right robot collects key k.
#     Bottom-right robot collects key j.
#     Top-right robot collects key l.
#     Bottom-left robot collects key n.
#     Bottom-left robot collects key m.
#     Bottom-left robot collects key o.
#
# This example requires at least 72 steps to collect all keys.
#
# After updating your map and using the remote-controlled robots, what is the fewest steps necessary to collect all of the keys?


def map_to_graphs(the_map: Matrix):
    graphs = []
    keys_to_collect = all_keys(the_map.values)

    for x, y in [x for x in the_map.index_range() if the_map.get(*x) == "@"]:
        graph = Graph()
        paths_from_start = find_edges_at(the_map, (x, y), keys_to_collect)
        for k, v in paths_from_start.items():
            graph.put("@", k, *v)

        keys_in_graph = set(paths_from_start.keys())
        while len(keys_in_graph) > 0:
            key = keys_in_graph.pop()
            paths = find_edges(the_map, key, keys_in_graph)
            for k, v in paths.items():
                graph.put(key, k, *v)

        graphs.append(graph)

    return graphs


def walk_graphs(graphs: List[Graph], start_at: str) -> int:

    # BFS
    # first position of the Walker now contains all current nodes
    w0 = (start_at * len(graphs), start_at)
    initial_walker = (w0, set())
    search_front = PriorityQueue()
    search_front.put((0, initial_walker))
    visited = set()
    target = "".join(sorted(set("".join(list(map(lambda x: x.all_nodes(), graphs))))))

    while not search_front.empty():
        # get top of queue
        (distance, walker_with_doors) = search_front.get()

        # check for target
        (walker, open_doors) = walker_with_doors
        (_, collected_keys) = walker
        if collected_keys == target:
            return distance

        # skip if visited
        if walker in visited:
            continue
        else:
            visited.add(walker)

        # expand and push in queue
        (multi_walker, doors) = walker_with_doors
        for i, g in enumerate(graphs):
            single_walker = multi_walker[0][i], multi_walker[1]
            for dw, expanded_walker in expand_walker((single_walker, doors), g):
                # shit code to expand each walker separately while keeping a single multiwalker state
                w = expanded_walker[0]
                new_walker = multi_walker[0][:i] + w[0] + multi_walker[0][i + 1:], w[1]
                search_front.put((distance + dw, (new_walker, expanded_walker[1])))

    return -1


if __name__ == "__main__":
    import time
    s_time = time.time()

    m = map_to_matrix(read_input("day18_part2"))
    gs = map_to_graphs(m)
    n = walk_graphs(gs, "@")
    print("Part Two: ", n)

    print("time: ", time.time() - s_time)
