from aoc09.tools.incode_computer import IntcodeComputer
from aoc09.util import read_input
from aoc09.tools.matrix import Matrix

# --- Day 19: Tractor Beam ---
#
# Unsure of the state of Santa's ship, you borrowed the tractor beam technology from Triton. Time to test it out.
#
# When you're safely away from anything else, you activate the tractor beam, but nothing happens. It's hard to tell whether it's working if there's nothing to use it on. Fortunately, your ship's drone system can be configured to deploy a drone to specific coordinates and then check whether it's being pulled. There's even an Intcode program (your puzzle input) that gives you access to the drone system.
#
# The program uses two input instructions to request the X and Y position to which the drone should be deployed. Negative numbers are invalid and will confuse the drone; all numbers should be zero or positive.
#
# Then, the program will output whether the drone is stationary (0) or being pulled by something (1). For example, the coordinate X=0, Y=0 is directly in front of the tractor beam emitter, so the drone control program will always report 1 at that location.
#
# To better understand the tractor beam, it is important to get a good picture of the beam itself. For example, suppose you scan the 10x10 grid of points closest to the emitter:
#
#        X
#   0->      9
#  0#.........
#  |.#........
#  v..##......
#   ...###....
#   ....###...
# Y .....####.
#   ......####
#   ......####
#   .......###
#  9........##
#
# In this example, the number of points affected by the tractor beam in the 10x10 area closest to the emitter is 27.
#
# However, you'll need to scan a larger area to understand the shape of the beam. How many points are affected by the tractor beam in the 50x50 area closest to the emitter? (For each of X and Y, this will be 0 through 49.)


def run_program(mem, x, y):
    comp = IntcodeComputer(mem)
    comp.run([x, y])
    return comp.output_list[-1]


if __name__ == '__main__':
    the_input = list(map(int, read_input("day19", ",")))

    m = Matrix().init_from_elem(50, 20, ".")
    for x, y in m.index_range():
        is_pulled = run_program(the_input, x, y)
        if is_pulled == 1:
            m.set(x, y, "#")

    m.print_top_left(print_headers=True)

    beam_area = len(list(filter(lambda i: i == "#", m.values)))

    print()
    print("Part One: ", beam_area)

# --- Part Two ---
#
# You aren't sure how large Santa's ship is. You aren't even sure if you'll need to use this thing on Santa's ship, but it doesn't hurt to be prepared. You figure Santa's ship might fit in a 100x100 square.
#
# The beam gets wider as it travels away from the emitter; you'll need to be a minimum distance away to fit a square of that size into the beam fully. (Don't rotate the square; it should be aligned to the same axes as the drone grid.)
#
# For example, suppose you have the following tractor beam readings:
#
# #.......................................
# .#......................................
# ..##....................................
# ...###..................................
# ....###.................................
# .....####...............................
# ......#####.............................
# ......######............................
# .......#######..........................
# ........########........................
# .........#########......................
# ..........#########.....................
# ...........##########...................
# ...........############.................
# ............############................
# .............#############..............
# ..............##############............
# ...............###############..........
# ................###############.........
# ................#################.......
# .................########OOOOOOOOOO.....
# ..................#######OOOOOOOOOO#....
# ...................######OOOOOOOOOO###..
# ....................#####OOOOOOOOOO#####
# .....................####OOOOOOOOOO#####
# .....................####OOOOOOOOOO#####
# ......................###OOOOOOOOOO#####
# .......................##OOOOOOOOOO#####
# ........................#OOOOOOOOOO#####
# .........................OOOOOOOOOO#####
# ..........................##############
# ..........................##############
# ...........................#############
# ............................############
# .............................###########
#
# In this example, the 10x10 square closest to the emitter that fits entirely within the tractor beam has been marked O. Within it, the point closest to the emitter (the only highlighted O) is at X=25, Y=20.
#
# Find the 100x100 square closest to the emitter that fits entirely within the tractor beam; within that square, find the point closest to the emitter. What value do you get if you take that point's X coordinate, multiply it by 10000, then add the point's Y coordinate? (In the example above, this would be 250020.)

    # The two borders of the beam are f and g (the coefficients are obtained experimentally from Part One)

# as respect to the beam
IN = 1
ON_LINE = 0
OUT = -1

if __name__ == '__main__':
    the_input = list(map(int, read_input("day19", ",")))

    def run_program(x, y):
        comp = IntcodeComputer(the_input)
        comp.run([x, y])
        return comp.output_list[-1]

    def bottom_line_position(x, y):
        it = run_program(x, y)
        below = run_program(x, y + 1)
        if it == 1 and below == 0:
            return ON_LINE
        elif it == 1:
            return IN
        else:
            return OUT

    def top_line_position(x, y):
        it = run_program(x, y)
        above = run_program(x, y - 1)
        if it == 1 and above == 0:
            return ON_LINE
        elif it == 1:
            return IN
        else:
            return OUT


    def find_square(x, y):
        while True:
            bottom = bottom_line_position(x, y)
            top = top_line_position(x + 99, y - 99)

            print(x, y, top, bottom)

            if bottom == ON_LINE and top == ON_LINE:
                break
            else:
                dx = 0
                dy = 0
                if bottom == IN:
                    dx = -1
                elif bottom == OUT:
                    dx = 1
                elif top == IN:
                    dy = -1
                elif top == OUT:
                    dy = 1

                x = x + dx
                y = y + dy

        return x, y - 99

    f_coef = sum([23.0/49.0, 14.0/30.0]) / 2.0
    g_coef = sum([29.0/49.0, 17.0/30.0]) / 2.0

    def f(x):
        return f_coef * x

    def g(x):
        return g_coef * x

    x1 = round((f(99) + 99) / (g_coef - f_coef))
    y1 = round(g(x1))

    # it depends if you are coming from the top or from the bottom!
    x, y = find_square(950, 550)

    print("Part Two: ", x * 10000 + y)
