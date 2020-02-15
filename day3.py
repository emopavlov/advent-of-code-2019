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


class NoIntersection:
    def __init__(self):
        pass


no_intersection = NoIntersection()


def invert(x):
    if isinstance(x, Location):
        return Location(x.y, x.x)
    elif isinstance(x, Section):
        return Section(
            invert(x.internal.start),
            invert(x.internal.end)
        )
    elif isinstance(x, NoIntersection):
        return x
    else:
        print("I can't invert this")


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y


class Section:
    class Vertical:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.x = start.x

    class Horizontal:
        def __init__(self, start, end):
            self.start = start
            self.end = end
            self.y = start.y

    def __init__(self, a, b):
        if a.x == b.x:  # vertical
            start = Location(a.x, min(a.y, b.y))
            end = Location(a.x, max(a.y, b.y))
            self.internal = Section.Vertical(start, end)
        elif a.y == b.y:  # horizontal
            start = Location(min(a.x, b.x), a.y)
            end = Location(max(a.x, b.x), a.y)
            self.internal = Section.Horizontal(start, end)
        else:
            print("ERROR. Only horizontal and vertical supported")

    def __eq__(self, other):
        return self.internal.start == other.start and self.internal.end == other.end

    def __ne__(self, other):
        return self.internal.start != other.start or self.internal.end != other.end

    def intersection(self, other):
        if isinstance(self.internal, Section.Vertical):
            if isinstance(other.internal, Section.Vertical):
                if self.internal.x != other.internal.x:
                    return no_intersection
                else:
                    start = max(self.internal.start.y, other.internal.start.y)
                    end = min(self.internal.end.y, other.internal.end.y)
                    if start == end:
                        return Location(self.internal.x, end)
                    elif start < end:
                        return Section(Location(self.internal.x, start), Location(self.internal.x, end))
                    else:
                        return no_intersection
            else:
                if self.internal.start.y <= other.internal.y <= self.internal.end.y and \
                        other.internal.start.x <= self.internal.x <= other.internal.end.x:
                    return Location(self.internal.x, other.internal.y)
                else:
                    return no_intersection
        else:
            return invert(invert(self).intersection(invert(other)))


class Wire:
    def __init__(self, path):
        self.sections = []
        start = Location(0, 0)
        for leg in path:
            end = Wire._section_end(start, leg)
            self.sections.append(Section(start, end))
            start = end

    @staticmethod
    def _section_end(start, leg):
        direction = leg[0]
        distance = int(leg[1:])
        if direction == "U":
            return Location(start.x, start.y + distance)
        elif direction == "D":
            return Location(start.x, start.y - distance)
        elif direction == "R":
            return Location(start.x + distance, start.y)
        elif direction == "L":
            return Location(start.x - distance, start.y)
        else:
            print("EXCEPTION! WTF")


def manhattan_distance(l1, l2):
    return abs(l1.x - l2.x) + abs(l1.y - l2.y)


day_3_input = util.read_input("day3")
path1 = day_3_input[0].split(",")
path2 = day_3_input[1].split(",")

min_distance = 10000000  # Something big

wire1 = Wire(path1)
wire2 = Wire(path2)
for s1 in wire1.sections:
    for s2 in wire2.sections:
        the_x = s1.intersection(s2)
        if isinstance(the_x, Location) and the_x != Location(0, 0):
            min_distance = min(min_distance, manhattan_distance(Location(0, 0), the_x))
        elif isinstance(the_x, Section):
            min_x = min(map(abs, range(the_x.start.x, the_x.end.x)))
            min_y = min(map(abs, range(the_x.start.y, the_x.end.y)))
            closest = Location(min_x, min_y)
            if closest != Location(0, 0):
                min_distance = min(min_distance, manhattan_distance(Location(0, 0), closest))

print("Part One", min_distance)


# --- Part Two ---
#
# It turns out that this circuit is very timing-sensitive; you actually need to minimize the signal delay.
#
# To do this, calculate the number of steps each wire takes to reach each intersection; choose the intersection where the sum of both wires' steps is lowest. If a wire visits a position on the grid multiple times, use the steps value from the first time it visits that position when calculating the total value of a specific intersection.
#
# The number of steps a wire takes is the total number of grid squares the wire has entered to get to that location, including the intersection being considered. Again consider the example from above:
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
# In the above example, the intersection closest to the central port is reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second wire for a total of 20+20 = 40 steps.
#
# However, the top-right intersection is better: the first wire takes only 8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.
#
# Here are the best steps for the extra examples from above:
#
#     R75,D30,R83,U83,L12,D49,R71,U7,L72
#     U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
#     R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
#     U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps
#
# What is the fewest combined steps the wires must take to reach an intersection?

print("Part Two", None)
