from aoc09.util import read_input
from aoc09.tools.matrix import Matrix
from typing import Tuple, List, Set
import string

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

Position = Tuple[int, int, str]  # x, y, keys collected


def keys(pos: Position) -> str:
    return pos[2]


def is_door(tile: chr) -> bool:
    return "A" <= tile <= "Z"


def is_key(tile: chr) -> bool:
    return "a" <= tile <= "z"


def all_keys(the_map: List[str]) -> str:
    return "".join(sorted(filter(is_key, '\n'.join(the_map))))


def map_to_matrix(the_map: List[str]) -> Matrix:
    m = Matrix()
    m.init_from_string('\n'.join(the_map))
    return m


def number_of_moves_to_collect_all_keys(the_map: Matrix) -> int:
    start_tile = the_map.index_of(START)
    target_keys = all_keys(the_map.values)

    def legal_moves(pos: Position) -> Set[Position]:
        x, y, ks = pos  # todo ks is searched, should be set instead

        def accessible(tile):
            x, y = tile
            if 0 <= x < the_map.width and 0 <= y < the_map.height:
                tile_value = the_map.get(x, y)
                return (tile_value == OPEN or
                        tile_value == START or
                        is_key(tile_value) or
                        is_door(tile_value) and tile_value.lower() in ks
                        )
            else:
                return False

        moves = [
            (x, y + 1),
            (x, y - 1),
            (x + 1, y),
            (x - 1, y)
        ]
        positions = set(map(lambda x: move_to_position(x[0], x[1], ks), filter(accessible, moves)))
        return positions

    def move_to_position(x, y, collected_keys):
        key = the_map.get(x, y)
        if is_key(key) and key not in collected_keys:
            return x, y, ''.join(sorted(collected_keys + key))
        else:
            return x, y, collected_keys

    start = start_tile + ("",)
    search_front = {start}
    visited = {start}
    steps = 0
    while len(search_front) > 0:
        for p in search_front:
            if keys(p) == target_keys:
                # Found it!
                return steps

        expanded_front = {m for pos in search_front for m in legal_moves(pos) if m not in visited}
        # increment and repeat
        search_front = expanded_front
        visited = visited.union(search_front)
        steps += 1

    return -1  # not found


if __name__ == "__main__":
    m = map_to_matrix(read_input("day18"))
    n = number_of_moves_to_collect_all_keys(m)
    print("Day 18:", n)
