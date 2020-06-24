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

    m = Matrix().init_from_elem(50, 50, ".")
    for x, y in m.index_range():
        is_pulled = run_program(the_input, x, y)
        if is_pulled == 1:
            m.set(x, y, "#")

    m.print_top_left(print_headers=True)

    beam_area = len(list(filter(lambda i: i == "#", m.values)))

    print()
    print("Part One: ", beam_area)
