from aoc09.util import read_input
from aoc09.tools.incode_computer import IntcodeComputer
from aoc09.tools.map import Map, Location

# map legend
empty = "."
wall = "#"
unexplored = " "
target = "X"
oxidised = "O"

# directions
N = 1
S = 2
W = 3
E = 4

# droid responses
hit_wall = 0
moved = 1
moved_to_target = 2


class Droid:
    def __init__(self, computer, location):
        self.droid_computer = computer.copy()
        self.droid_location = Location(location.x, location.y)
        self.path_length = 0

    def copy(self):
        other = Droid(self.droid_computer, self.droid_location)
        other.path_length = self.path_length
        return other

    def split_and_move(self):
        moves = {
            N: area_map.get(self.droid_location.x, self.droid_location.y + 1, unexplored),
            S: area_map.get(self.droid_location.x, self.droid_location.y - 1, unexplored),
            E: area_map.get(self.droid_location.x + 1, self.droid_location.y, unexplored),
            W: area_map.get(self.droid_location.x - 1, self.droid_location.y, unexplored)
        }
        eligible_moves = dict(filter(lambda elem: elem[1] == unexplored or elem[1] == target, moves.items()))

        new_copies = [self.copy() for i in range(0, len(eligible_moves.keys()))]
        for droid, dir in zip(new_copies, eligible_moves.keys()):
            droid.droid_computer.continue_run([dir])
            droid.path_length += 1  # this includes attempted moves that hit a wall
            if dir == N:
                droid.droid_location.move_north()
            elif dir == S:
                droid.droid_location.move_south()
            elif dir == E:
                droid.droid_location.move_east()
            elif dir == W:
                droid.droid_location.move_west()

        return new_copies

    def get_result(self):
        return self.droid_computer.output_list[-1]


def update_map(droid):
    result = droid.get_result()
    if result == hit_wall:
        area_map.set(droid.droid_location.x, droid.droid_location.y, wall)
    elif result == moved:
        area_map.set(droid.droid_location.x, droid.droid_location.y, empty)
    elif result == moved_to_target:
        area_map.set(droid.droid_location.x, droid.droid_location.y, target)


def prune(droids):
    def success(droid):
        return (droid.get_result() == moved_to_target or droid.get_result() == moved) and \
                area_map.get(droid.droid_location.x, droid.droid_location.y, unexplored) == unexplored

    return list(filter(success, droids))


def bfs(droid, explore_mode=False):
    droids = [droid]
    step_count = 0

    while len(droids) > 0:
        expanded_droids = []
        for droid in droids:
            new_copies = droid.split_and_move()
            eligible_copies = prune(new_copies)
            for d in eligible_copies:
                if (not explore_mode) and d.get_result() == moved_to_target:
                    print("Part One", d.path_length)
                    return d

                update_map(d)

            expanded_droids = expanded_droids + eligible_copies
        droids = expanded_droids
        step_count += 1

    return step_count


# --- Day 15: Oxygen System ---
#
# Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!
#
# According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated repair droid is your only option for fixing the oxygen system.
#
# The Elves' care package included an Intcode program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.
#
# The remote control program executes the following steps in a loop forever:
#
#     Accept a movement command via an input instruction.
#     Send the movement command to the repair droid.
#     Wait for the repair droid to finish the movement operation.
#     Report on the status of the repair droid via an output instruction.
#
# Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.
#
# The repair droid can reply with any of the following status codes:
#
#     0: The repair droid hit a wall. Its position has not changed.
#     1: The repair droid has moved one step in the requested direction.
#     2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
#
# You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.
#
# For example, we can draw the area using D for the droid, # for walls, . for locations the droid can traverse, and empty space for unexplored locations. Then, the initial state looks like this:
#
#
#
#    D
#
#
#
# To make the droid go north, send it 1. If it replies with 0, you know that location is a wall and that the droid didn't move:
#
#
#    #
#    D
#
#
#
# To move east, send 4; a reply of 1 means the movement was successful:
#
#
#    #
#    .D
#
#
#
# Then, perhaps attempts to move north (1), south (2), and east (4) are all met with replies of 0:
#
#
#    ##
#    .D#
#     #
#
#
# Now, you know the repair droid is in a dead end. Backtrack with 3 (which you already know will get a reply of 1 because you already know that location is open):
#
#
#    ##
#    D.#
#     #
#
#
# Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south again (2) gets a reply of 0, and then west (3) gets a reply of 2:
#
#
#    ##
#   #..#
#   D.#
#    #
#
# Now, because of the reply of 2, you know you've found the oxygen system! In this example, it was only 2 moves away from the repair droid's starting position.
#
# What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?

program = list(map(int, read_input("day15", ",")))
droid_computer = IntcodeComputer(program)
area_map = Map()
droid_location = Location(0, 0)
area_map.set(0, 0, empty)

droid_on_target = bfs(Droid(droid_computer, droid_location))


# --- Part Two ---
#
# You quickly repair the oxygen system; oxygen gradually fills the area.
#
# Oxygen starts in the location containing the repaired oxygen system. It takes one minute for oxygen to spread to all open locations that are adjacent to a location that already contains oxygen. Diagonal locations are not adjacent.
#
# In the example above, suppose you've used the droid to explore the area fully and have the following map (where locations that currently contain oxygen are marked O):
#
#  ##
# #..##
# #.#..#
# #.O.#
#  ###
#
# Initially, the only location which contains oxygen is the location of the repaired oxygen system. However, after one minute, the oxygen spreads to all open (.) locations that are adjacent to a location containing oxygen:
#
#  ##
# #..##
# #.#..#
# #OOO#
#  ###
#
# After a total of two minutes, the map looks like this:
#
#  ##
# #..##
# #O#O.#
# #OOO#
#  ###
#
# After a total of three minutes:
#
#  ##
# #O.##
# #O#OO#
# #OOO#
#  ###
#
# And finally, the whole region is full of oxygen after a total of four minutes:
#
#  ##
# #OO##
# #O#OO#
# #OOO#
#  ###
#
# So, in this example, all locations contain oxygen after 4 minutes.
#
# Use the repair droid to get a complete map of the area. How many minutes will it take to fill with oxygen?


area_map = Map()  # clean up map
steps = bfs(droid_on_target, explore_mode=True)
print("Part Two", steps - 1)  # last round nothing expands
