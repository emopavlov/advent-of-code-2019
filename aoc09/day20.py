from aoc09.tools.search import *
from aoc09.tools.matrix import Matrix
from aoc09 import util
import string
from typing import Set, Dict

# --- Day 20: Donut Maze ---
#
# You notice a strange pattern on the surface of Pluto and land nearby to get a closer look. Upon closer inspection, you realize you've come across one of the famous space-warping mazes of the long-lost Pluto civilization!
#
# Because there isn't much space on Pluto, the civilization that used to live here thrived by inventing a method for folding spacetime. Although the technology is no longer understood, mazes like this one provide a small glimpse into the daily life of an ancient Pluto citizen.
#
# This maze is shaped like a donut. Portals along the inner and outer edge of the donut can instantly teleport you from one side to the other. For example:
#
#          A
#          A
#   #######.#########
#   #######.........#
#   #######.#######.#
#   #######.#######.#
#   #######.#######.#
#   #####  B    ###.#
# BC...##  C    ###.#
#   ##.##       ###.#
#   ##...DE  F  ###.#
#   #####    G  ###.#
#   #########.#####.#
# DE..#######...###.#
#   #.#########.###.#
# FG..#########.....#
#   ###########.#####
#              Z
#              Z
#
# This map of the maze shows solid walls (#) and open passages (.). Every maze on Pluto has a start (the open tile next to AA) and an end (the open tile next to ZZ). Mazes on Pluto also have portals; this maze has three pairs of portals: BC, DE, and FG. When on an open tile next to one of these labels, a single step can take you to the other tile with the same label. (You can only walk on . tiles; labels and empty space are not traversable.)
#
# One path through the maze doesn't require any portals. Starting at AA, you could go down 1, right 8, down 12, left 4, and down 1 to reach ZZ, a total of 26 steps.
#
# However, there is a shorter path: You could walk from AA to the inner BC portal (4 steps), warp to the outer BC portal (1 step), walk to the inner DE (6 steps), warp to the outer DE (1 step), walk to the outer FG (4 steps), warp to the inner FG (1 step), and finally walk to ZZ (6 steps). In total, this is only 23 steps.
#
# Here is a larger example:
#
#                    A
#                    A
#   #################.#############
#   #.#...#...................#.#.#
#   #.#.#.###.###.###.#########.#.#
#   #.#.#.......#...#.....#.#.#...#
#   #.#########.###.#####.#.#.###.#
#   #.............#.#.....#.......#
#   ###.###########.###.#####.#.#.#
#   #.....#        A   C    #.#.#.#
#   #######        S   P    #####.#
#   #.#...#                 #......VT
#   #.#.#.#                 #.#####
#   #...#.#               YN....#.#
#   #.###.#                 #####.#
# DI....#.#                 #.....#
#   #####.#                 #.###.#
# ZZ......#               QG....#..AS
#   ###.###                 #######
# JO..#.#.#                 #.....#
#   #.#.#.#                 ###.#.#
#   #...#..DI             BU....#..LF
#   #####.#                 #.#####
# YN......#               VT..#....QG
#   #.###.#                 #.###.#
#   #.#...#                 #.....#
#   ###.###    J L     J    #.#.###
#   #.....#    O F     P    #.#...#
#   #.###.#####.#.#####.#####.###.#
#   #...#.#.#...#.....#.....#.#...#
#   #.#####.###.###.#.#.#########.#
#   #...#.#.....#...#.#.#.#.....#.#
#   #.###.#####.###.###.#.#.#######
#   #.#.........#...#.............#
#   #########.###.###.#############
#            B   J   C
#            U   P   P
#
# Here, AA has no direct path to ZZ, but it does connect to AS and CP. By passing through AS, QG, BU, and JO, you can reach ZZ in 58 steps.
#
# In your maze, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ?

PORTALS = string.ascii_uppercase
OPEN = "."
ACCESSIBLE = PORTALS + OPEN


def portals(m: Matrix) -> Set[Target]:
    def portal_position(p1, p2):
        if p1[0] == p2[0]:  # x
            x = p1[0]
            y1, y2 = p1[1], p2[1]
            if 0 <= y1 - 1 and m.get(x, y1 - 1) == OPEN:
                return x, y1 - 1
            else:
                return x, y2 + 1
        else:  # y
            y = p1[1]
            x1, x2 = p1[0], p2[0]
            if 0 <= x1 - 1 and m.get(x1 - 1, y) == OPEN:
                return x1 - 1, y
            else:
                return x2 + 1, y

    def horizontal_portals_at(y: int):
        xs = [x for x in range(m.width) if m.get(x, y) in PORTALS and m.get(x, y + 1) in PORTALS]
        return [Target(*portal_position((x, y), (x, y + 1)), m.get(x, y) + m.get(x, y + 1)) for x in xs]

    def vertical_portals_at(x: int):
        ys = [y for y in range(m.height) if m.get(x, y) in PORTALS and m.get(x + 1, y) in PORTALS]
        return [Target(*portal_position((x, y), (x + 1, y)), m.get(x, y) + m.get(x + 1, y)) for y in ys]

    donut_width = 0
    mid_y = m.height // 2
    for x in range(2, m.width):
        if m.get(x, mid_y) == " ":
            if m.get(x, mid_y) in PORTALS:
                donut_width = x - 4  # 2 for the outer edge and 2 for the portal we just skipped
            else:
                donut_width = x - 2
            break

    outer_portals = horizontal_portals_at(0) + horizontal_portals_at(m.height - 2) + \
                    vertical_portals_at(0) + vertical_portals_at(m.width - 2)
    inner_portals = horizontal_portals_at(2 + donut_width) + horizontal_portals_at(m.height - 4 - donut_width) + \
                    vertical_portals_at(2 + donut_width) + vertical_portals_at(m.width - 4 - donut_width)

    return set(outer_portals).union(set(map(lambda t: Target(t.x, t.y, t.name + "X"), inner_portals)))


def expand(m: Matrix, target_positions: Set[Tuple[int, int]], x: int, y: int):
    x_expand = list(map(lambda x: (x, y), filter(lambda x: x >= 0 and x < m.width, [x + 1, x - 1])))
    y_expand = list(map(lambda y: (x, y), filter(lambda x: x >= 0 and x < m.height, [y + 1, y - 1])))
    return list(filter(lambda p: p in target_positions or m.get(*p) == OPEN, x_expand + y_expand))


def construct_graph(ps: Set[Target], m: Matrix):
    def maze_expand(x, y):
        return expand(m, set(map(lambda t: t.position(), ps)), x, y)

    graph = bfs_to_graph(ps, maze_expand)

    # add teleportation
    for name in list(map(lambda n: n.name, ps)):
        alt_name = name + "X"
        if graph.has_node(alt_name):
            graph.add_node(name, alt_name, 1)
            graph.add_node(alt_name, name, 1)

    return graph


if __name__ == "__main__":
    maze = util.read_input("day20", should_strip=False)
    m = Matrix()
    m.init_from_string('\n'.join(maze))
    ps = portals(m)

    g = construct_graph(ps, m)
    min_distance = dijkstra(g, "AA", "ZZ")

    print("Part Onw: ", min_distance)

# --- Part Two ---
#
# Strangely, the exit isn't open when you reach it. Then, you remember: the ancient Plutonians were famous for building recursive spaces.
#
# The marked connections in the maze aren't portals: they physically connect to a larger or smaller copy of the maze. Specifically, the labeled tiles around the inside edge actually connect to a smaller copy of the same maze, and the smaller copy's inner labeled tiles connect to yet a smaller copy, and so on.
#
# When you enter the maze, you are at the outermost level; when at the outermost level, only the outer labels AA and ZZ function (as the start and end, respectively); all other outer labeled tiles are effectively walls. At any other level, AA and ZZ count as walls, but the other outer labeled tiles bring you one level outward.
#
# Your goal is to find a path through the maze that brings you back to ZZ at the outermost level of the maze.
#
# In the first example above, the shortest path is now the loop around the right side. If the starting level is 0, then taking the previously-shortest path would pass through BC (to level 1), DE (to level 2), and FG (back to level 1). Because this is not the outermost level, ZZ is a wall, and the only option is to go back around to BC, which would only send you even deeper into the recursive maze.
#
# In the second example above, there is no path that brings you to ZZ at the outermost level.
#
# Here is a more interesting example:
#
#              Z L X W       C
#              Z P Q B       K
#   ###########.#.#.#.#######.###############
#   #...#.......#.#.......#.#.......#.#.#...#
#   ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###
#   #.#...#.#.#...#.#.#...#...#...#.#.......#
#   #.###.#######.###.###.#.###.###.#.#######
#   #...#.......#.#...#...#.............#...#
#   #.#########.#######.#.#######.#######.###
#   #...#.#    F       R I       Z    #.#.#.#
#   #.###.#    D       E C       H    #.#.#.#
#   #.#...#                           #...#.#
#   #.###.#                           #.###.#
#   #.#....OA                       WB..#.#..ZH
#   #.###.#                           #.#.#.#
# CJ......#                           #.....#
#   #######                           #######
#   #.#....CK                         #......IC
#   #.###.#                           #.###.#
#   #.....#                           #...#.#
#   ###.###                           #.#.#.#
# XF....#.#                         RF..#.#.#
#   #####.#                           #######
#   #......CJ                       NM..#...#
#   ###.#.#                           #.###.#
# RE....#.#                           #......RF
#   ###.###        X   X       L      #.#.#.#
#   #.....#        F   Q       P      #.#.#.#
#   ###.###########.###.#######.#########.###
#   #.....#...#.....#.......#...#.....#.#...#
#   #####.#.###.#######.#######.###.###.#.#.#
#   #.......#.......#.#.#.#.#...#...#...#.#.#
#   #####.###.#####.#.#.#.#.###.###.#.###.###
#   #.......#.....#.#...#...............#...#
#   #############.#.#.###.###################
#                A O F   N
#                A A D   M
#
# One shortest path through the maze is the following:
#
#     Walk from AA to XF (16 steps)
#     Recurse into level 1 through XF (1 step)
#     Walk from XF to CK (10 steps)
#     Recurse into level 2 through CK (1 step)
#     Walk from CK to ZH (14 steps)
#     Recurse into level 3 through ZH (1 step)
#     Walk from ZH to WB (10 steps)
#     Recurse into level 4 through WB (1 step)
#     Walk from WB to IC (10 steps)
#     Recurse into level 5 through IC (1 step)
#     Walk from IC to RF (10 steps)
#     Recurse into level 6 through RF (1 step)
#     Walk from RF to NM (8 steps)
#     Recurse into level 7 through NM (1 step)
#     Walk from NM to LP (12 steps)
#     Recurse into level 8 through LP (1 step)
#     Walk from LP to FD (24 steps)
#     Recurse into level 9 through FD (1 step)
#     Walk from FD to XQ (8 steps)
#     Recurse into level 10 through XQ (1 step)
#     Walk from XQ to WB (4 steps)
#     Return to level 9 through WB (1 step)
#     Walk from WB to ZH (10 steps)
#     Return to level 8 through ZH (1 step)
#     Walk from ZH to CK (14 steps)
#     Return to level 7 through CK (1 step)
#     Walk from CK to XF (10 steps)
#     Return to level 6 through XF (1 step)
#     Walk from XF to OA (14 steps)
#     Return to level 5 through OA (1 step)
#     Walk from OA to CJ (8 steps)
#     Return to level 4 through CJ (1 step)
#     Walk from CJ to RE (8 steps)
#     Return to level 3 through RE (1 step)
#     Walk from RE to IC (4 steps)
#     Recurse into level 4 through IC (1 step)
#     Walk from IC to RF (10 steps)
#     Recurse into level 5 through RF (1 step)
#     Walk from RF to NM (8 steps)
#     Recurse into level 6 through NM (1 step)
#     Walk from NM to LP (12 steps)
#     Recurse into level 7 through LP (1 step)
#     Walk from LP to FD (24 steps)
#     Recurse into level 8 through FD (1 step)
#     Walk from FD to XQ (8 steps)
#     Recurse into level 9 through XQ (1 step)
#     Walk from XQ to WB (4 steps)
#     Return to level 8 through WB (1 step)
#     Walk from WB to ZH (10 steps)
#     Return to level 7 through ZH (1 step)
#     Walk from ZH to CK (14 steps)
#     Return to level 6 through CK (1 step)
#     Walk from CK to XF (10 steps)
#     Return to level 5 through XF (1 step)
#     Walk from XF to OA (14 steps)
#     Return to level 4 through OA (1 step)
#     Walk from OA to CJ (8 steps)
#     Return to level 3 through CJ (1 step)
#     Walk from CJ to RE (8 steps)
#     Return to level 2 through RE (1 step)
#     Walk from RE to XQ (14 steps)
#     Return to level 1 through XQ (1 step)
#     Walk from XQ to FD (8 steps)
#     Return to level 0 through FD (1 step)
#     Walk from FD to ZZ (18 steps)
#
# This path takes a total of 396 steps to move from AA at the outermost layer to ZZ at the outermost layer.
#
# In your maze, when accounting for recursion, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ, both at the outermost layer?


Node2 = Tuple[str, int]  # name, level


class RecursiveGraph(Graph):
    """
    A special implementation of Graph which supports multiple graph levels as defined in the task
    """

    def __init__(self, graph: Graph):
        self.inner = graph

    def add_node(self, source, destination, distance):
        raise NotImplementedError

    def has_node(self, node):
        raise NotImplementedError

    def distance(self, source: Node2, destination: Node2) -> int:
        s_name, s_level = source
        d_name, d_level = destination

        if s_level == d_level:
            return self.inner.distance(s_name, d_name)

        # add teleportation
        elif s_name[-1] == "X" and s_name[0:2] == d_name and s_level == d_level - 1:
            return 1

        elif d_name[-1] == "X" and d_name[0:2] == s_name and s_level == d_level + 1:
            return 1

        raise Exception(f"No edge from {source} to {destination}")

    def neighbours(self, node: Node2) -> Dict[Node2, int]:
        name, level = node
        ns = self.inner.neighbours(name)

        neighbours = dict(map(lambda k: ((k, level), ns[k]), ns))
        if self.__is_inner(name):
            neighbours[(name[0:2], level + 1)] = 1
        elif level > 1 and name != "AA" and name != "ZZ":  # is outer
            neighbours[(name + "X", level - 1)] = 1

        return neighbours

    def __repr__(self):
        return self.inner.__repr__()

    def __is_inner(self, name):
        return name[-1] == "X"


def construct_recursive_graph(ps: Set[Target], m: Matrix):
    def maze_expand(x, y):
        return expand(m, set(map(lambda t: t.position(), ps)), x, y)

    graph = bfs_to_graph(ps, maze_expand)
    rgraph = RecursiveGraph(graph)
    return rgraph


if __name__ == "__main__":
    maze = util.read_input("day20", should_strip=False)
    m = Matrix()
    m.init_from_string('\n'.join(maze))
    ps = portals(m)
    g = construct_recursive_graph(ps, m)
    min_distance = dijkstra(g, ("AA", 1), ("ZZ", 1))

    print("Part Two: ", min_distance)
