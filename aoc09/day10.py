from aoc09.util import read_input
from aoc09.tools.matrix import Matrix


# --- Day 10: Monitoring Station ---
#
# You fly into the asteroid belt and reach the Ceres monitoring station. The Elves here have an emergency: they're having trouble tracking all of the asteroids and can't be sure they're safe.
#
# The Elves would like to build a new monitoring station in a nearby area of space; they hand you a map of all of the asteroids in that region (your puzzle input).
#
# The map indicates whether each position is empty (.) or contains an asteroid (#). The asteroids are much smaller than they appear on the map, and every asteroid is exactly in the center of its marked position. The asteroids can be described with X,Y coordinates where X is the distance from the left edge and Y is the distance from the top edge (so the top-left corner is 0,0 and the position immediately to its right is 1,0).
#
# Your job is to figure out which asteroid would be the best place to build a new monitoring station. A monitoring station can detect any asteroid to which it has direct line of sight - that is, there cannot be another asteroid exactly between them. This line of sight can be at any angle, not just lines aligned to the grid or diagonally. The best location is the asteroid that can detect the largest number of other asteroids.
#
# For example, consider the following map:
#
# .#..#
# .....
# #####
# ....#
# ...##
#
# The best location for a new monitoring station on this map is the highlighted asteroid at 3,4 because it can detect 8 asteroids, more than any other location. (The only asteroid it cannot detect is the one at 1,0; its view of this asteroid is blocked by the asteroid at 2,2.) All other asteroids are worse locations; they can detect 7 or fewer other asteroids. Here is the number of other asteroids a monitoring station on each asteroid could detect:
#
# .7..7
# .....
# 67775
# ....7
# ...87
#
# Here is an asteroid (#) and some examples of the ways its line of sight might be blocked. If there were another asteroid at the location of a capital letter, the locations marked with the corresponding lowercase letter would be blocked and could not be detected:
#
# #.........
# ...A......
# ...B..a...
# .EDCG....a
# ..F.c.b...
# .....c....
# ..efd.c.gb
# .......c..
# ....f...c.
# ...e..d..c
#
# Here are some larger examples:
#
#     Best is 5,8 with 33 other asteroids detected:
#
#     ......#.#.
#     #..#.#....
#     ..#######.
#     .#.#.###..
#     .#..#.....
#     ..#....#.#
#     #..#....#.
#     .##.#..###
#     ##...#..#.
#     .#....####
#
#     Best is 1,2 with 35 other asteroids detected:
#
#     #.#...#.#.
#     .###....#.
#     .#....#...
#     ##.#.#.#.#
#     ....#.#.#.
#     .##..###.#
#     ..#...##..
#     ..##....##
#     ......#...
#     .####.###.
#
#     Best is 6,3 with 41 other asteroids detected:
#
#     .#..#..###
#     ####.###.#
#     ....###.#.
#     ..###.##.#
#     ##.##.#.#.
#     ....###..#
#     ..#.#..#.#
#     #..#.#.###
#     .##...##.#
#     .....#.#..
#
#     Best is 11,13 with 210 other asteroids detected:
#
#     .#..##.###...#######
#     ##.############..##.
#     .#.######.########.#
#     .###.#######.####.#.
#     #####.##.#.##.###.##
#     ..#####..#.#########
#     ####################
#     #.####....###.#.#.##
#     ##.#################
#     #####.##.###..####..
#     ..######..##.#######
#     ####.##.####...##..#
#     .#####..#.######.###
#     ##...#.##########...
#     #.##########.#######
#     .####.#.###.###.#.##
#     ....##.##.###..#####
#     .#.#.###########.###
#     #.#.#.#####.####.###
#     ###.##.####.##.#..##
#
# Find the best location for a new monitoring station. How many other asteroids can be detected from that location?


def to_matrix(lines):
    return Matrix().init_from_values(list(map(list, lines)))


def spiral_search(f, matrix, c):
    (cx, cy) = c[0], c[1]

    def in_bounds(index):
        return 0 <= index[0] < matrix.width and 0 <= index[1] < matrix.height

    d = 0
    circle = [c]

    # moving clockwise starting from top left
    while len(circle) > 0:
        d += 1
        circle = list(filter(in_bounds, (list(map(lambda x: (x, cy - d), range(cx - d, cx + d + 1)))))) + \
                 list(filter(in_bounds, (list(map(lambda y: (cx + d, y), range(cy - d + 1, cy + d)))))) + \
                 list(filter(in_bounds, (list(map(lambda x: (x, cy + d), range(cx + d, cx - d, -1)))))) + \
                 list(filter(in_bounds, (list(map(lambda y: (cx - d, y), range(cy + d, cy - d, -1))))))

        for a in circle:
            f(matrix.get(a[0], a[1]))


def vector(p1, p2):
    return p2[0] - p1[0], p2[1] - p1[1]


def find_hidden(p1, p2, matrix):
    (x1, y1), (x2, y2) = p1, p2
    hidden = []

    if x1 == x2:
        x = x1  # vertical
        (step, limit) = (1, matrix.height) if (y2 - y1) > 0 else (-1, -1)
        for y in range(y2 + step, limit, step):
            if matrix.get(x, y) == "#":
                hidden.append((x, y))
    else:
        # p1 + K * v = p, { p = all points hidden by p2 }  <=>  K = (p - p1) / v  =>
        # vy*(x - 1) + xv*y1 = vx*y  => y is int <=>  vy*(x - 1) + vx*y1 is divisible by vx
        vx, vy = vector(p1, p2)
        (step, limit) = (1, matrix.width) if (x2 - x1) > 0 else (-1, -1)
        for x in range(x2 + step, limit, step):
            a = (vy * (x - x1) + vx * y1)
            if a % vx == 0:
                y = a // vx
                if 0 <= y < matrix.height and matrix.get(x, y) == "#":
                    hidden.append((x, y))

    return hidden


def asteroids(matrix):
    return ((x, y) for (x, y) in matrix.index_range() if matrix.get(x, y) == "#")


def asteroid_visibility(a, matrix):
    x, y = a
    a_matrix = matrix.copy()
    a_matrix.set(x, y, "C")  # Don't count current
    for (ox, oy) in asteroids(a_matrix):
        for h in find_hidden((x, y), (ox, oy), a_matrix):
            a_matrix.set(h[0], h[1], "X")

    visible = a_matrix.values.count("#")
    return visible


def asteroid_with_best_visibility(matrix):
    max_visible = 0
    best = None
    for (x, y) in matrix.index_range():
        if matrix.get(x, y) == "#":
            visible = asteroid_visibility((x, y), matrix)
            if visible > max_visible:
                max_visible = visible
                best = (x, y)
    return best, max_visible


m = to_matrix(read_input("day10"))
winner = asteroid_with_best_visibility(m)
print("Part One:", winner)


# --- Part Two ---
#
# Once you give them the coordinates, the Elves quickly deploy an Instant Monitoring Station to the location and discover the worst: there are simply too many asteroids.
#
# The only solution is complete vaporization by giant laser.
#
# Fortunately, in addition to an asteroid scanner, the new monitoring station also comes equipped with a giant rotating laser perfect for vaporizing asteroids. The laser starts by pointing up and always rotates clockwise, vaporizing any asteroid it hits.
#
# If multiple asteroids are exactly in line with the station, the laser only has enough power to vaporize one of them before continuing its rotation. In other words, the same asteroids that can be detected can be vaporized, but if vaporizing one asteroid makes another one detectable, the newly-detected asteroid won't be vaporized until the laser has returned to the same position by rotating a full 360 degrees.
#
# For example, consider the following map, where the asteroid with the new monitoring station (and laser) is marked X:
#
# .#....#####...#..
# ##...##.#####..##
# ##...#...#.#####.
# ..#.....X...###..
# ..#.#.....#....##
#
# The first nine asteroids to get vaporized, in order, would be:
#
# .#....###24...#..
# ##...##.13#67..9#
# ##...#...5.8####.
# ..#.....X...###..
# ..#.#.....#....##
#
# Note that some asteroids (the ones behind the asteroids marked 1, 5, and 7) won't have a chance to be vaporized until the next full rotation. The laser continues rotating; the next nine to be vaporized are:
#
# .#....###.....#..
# ##...##...#.....#
# ##...#......1234.
# ..#.....X...5##..
# ..#.9.....8....76
#
# The next nine to be vaporized are then:
#
# .8....###.....#..
# 56...9#...#.....#
# 34...7...........
# ..2.....X....##..
# ..1..............
#
# Finally, the laser completes its first full rotation (1 through 3), a second rotation (4 through 8), and vaporizes the last asteroid (9) partway through its third rotation:
#
# ......234.....6..
# ......1...5.....7
# .................
# ........X....89..
# .................
#
# In the large example above (the one with the best monitoring station location at 11,13):
#
#     The 1st asteroid to be vaporized is at 11,12.
#     The 2nd asteroid to be vaporized is at 12,1.
#     The 3rd asteroid to be vaporized is at 12,2.
#     The 10th asteroid to be vaporized is at 12,8.
#     The 20th asteroid to be vaporized is at 16,0.
#     The 50th asteroid to be vaporized is at 16,9.
#     The 100th asteroid to be vaporized is at 10,16.
#     The 199th asteroid to be vaporized is at 9,6.
#     The 200th asteroid to be vaporized is at 8,2.
#     The 201st asteroid to be vaporized is at 10,9.
#     The 299th and final asteroid to be vaporized is at 11,1.
#
# The Elves are placing bets on which will be the 200th asteroid to be vaporized. Win the bet by determining which asteroid that will be; what do you get if you multiply its X coordinate by 100 and then add its Y coordinate? (For example, 8,2 becomes 802.)
