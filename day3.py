import util

# --- Day 3: Crossed Wires ---
#
# The gravity assist was successful, and you're well on your way to the Venus refuelling station. During the rush back on Earth, the fuel management system wasn't completely installed, so that's next on the priority list.
#
# Opening the front panel reveals a jumble of wires. Specifically, two wires are connected to a central port and extend outward on a grid. You trace the path each wire takes as it leaves the central port, one wire per line of text (your puzzle input).
#
# The wires twist and turn, but the two wires occasionally cross paths. To fix the circuit, you need to find the intersection point closest to the central port. Because the wires are on a grid, use the Manhattan distance for this measurement. While the wires do technically cross right at the central port where they both start, this point does not count, nor does a wire count as crossing with itself.
#
# For example, if the first wire's path is R8,U5,L5,D3, then starting from the central port (o), it goes right 8, up 5, left 5, and finally down 3:
#
# ...........
# ...........
# ...........
# ....+----+.
# ....|....|.
# ....|....|.
# ....|....|.
# .........|.
# .o-------+.
# ...........
#
# Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down 4, and left 4:
#
# ...........
# .+-----+...
# .|.....|...
# .|..+--X-+.
# .|..|..|.|.
# .|.-X--+.|.
# .|..|....|.
# .|.......|.
# .o-------+.
# ...........
#
# These wires cross at two locations (marked X), but the lower-left one is closer to the central port: its distance is 3 + 3 = 6.
#
# Here are a few more examples:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135
#
# What is the Manhattan distance from the central port to the closest intersection?


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Wire:
    def turn(self):
        self.path_index += 1
        if self.path_index >= len(self.path):
            self.location = None
        else:
            self.direction = self.path[self.path_index][0]
            self.distance_to_turn = int(self.path[self.path_index][1:]) - 1

    def move(self):
        if self.distance_to_turn == 0:
            self.turn()

        if self.has_next():  # check after turning
            if self.direction == "U":
                self.location.y += 1
            elif self.direction == "D":
                self.location.y -= 1
            elif self.direction == "R":
                self.location.x += 1
            elif self.direction == "L":
                self.location.x -= 1
            else:
                print("EXCEPTION! WTF")

        self.distance_to_turn -= 1

    def __init__(self, path):
        self.path = path.copy()
        self.location = Location(0, 0)
        self.path_index = -1
        self.distance_to_turn = 0
        self.direction = ""  # initialized at first turn

    def has_next(self):
        return self.location != None

    def next_location(self):
        current_location = Location(self.location.x, self.location.y)
        self.move()
        return current_location


def manhattan_distance(l1, l2):
    return abs(l1.x - l2.x) + abs(l1.y - l2.y)


def print_wire(wire):
    locations = []
    while wire.has_next():
        locations.append(wire.next_location())

    max_x = max(*list(map(lambda l: l.x, locations)))
    max_y = max(*list(map(lambda l: l.y, locations)))
    min_x = min(*list(map(lambda l: l.x, locations)))
    min_y = min(*list(map(lambda l: l.y, locations)))

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    board = util.Matrix(width, height, ".")

    for l in locations:
        board.set((l.x - min_x), (l.y - min_y), "O")

    board.print_bottom_left()


day_3_input = util.read_input("day3")
path1 = day_3_input[0].split(",")
# print_wire(Wire(path1))
path2 = day_3_input[1].split(",")
# print_wire(Wire(path2))

min_distance = 10000000  # Something big

wire1 = Wire(path1)
while wire1.has_next():
    l1 = wire1.next_location()
    wire2 = Wire(path2)
    while wire2.has_next():
        l2 = wire2.next_location()
        if (l1.x, l1.y) != (0, 0) and (l1.x, l1.y) == (l2.x, l2.y):
            min_distance = min(min_distance, manhattan_distance(Location(0, 0), l1))

print("Part One", min_distance)
