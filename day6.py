import util

# --- Day 6: Universal Orbit Map ---
#
# You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often involves transferring between orbits, the orbit maps here are useful for finding efficient routes between, for example, you and Santa. You download a map of the local orbits (your puzzle input).
#
# Except for the universal Center of Mass (COM), every object in space is in orbit around exactly one other object. An orbit looks roughly like this:
#
#                   \
#                    \
#                     |
#                     |
# AAA--> o            o <--BBB
#                     |
#                     |
#                    /
#                   /
#
# In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA (drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, which means "BBB is in orbit around AAA".
#
# Before you use your map data to plot a course, you need to make sure it wasn't corrupted during the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total number of direct orbits (like the one shown above) and indirect orbits.
#
# Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
#
# Visually, the above map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I
#
# In this visual representation, when two objects are connected by a line, the one on the right directly orbits the one on the left.
#
# Here, we can count the total number of orbits as follows:
#
#     D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
#     L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
#     COM orbits nothing.
#
# The total number of direct and indirect orbits in this example is 42.
#
# What is the total number of direct and indirect orbits in your map data?

the_input = util.read_input("day6_test")

orbit_map = {}
for line in the_input:
    (center, satellite) = line.split(")")
    if center in orbit_map:
        orbit_map[center].append(satellite)
    else:
        orbit_map[center] = [satellite]

print(orbit_map)


def walk(node, depth=0, path=[]):
    """ iterate tree in pre-order depth-first search order """
    yield node, depth, path + [node]
    if node in orbit_map:
        for child in orbit_map[node]:
            for n in walk(child, depth + 1, path + [node]):
                yield n


print("Part One:", sum(map(lambda x: x[1], walk("COM"))))


# --- Part Two ---
#
# Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).
#
# You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.
#
# For example, suppose you have the following map:
#
# COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L
# K)YOU
# I)SAN
#
# Visually, the above map of orbits looks like this:
#
#                           YOU
#                          /
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#
# In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:
#
#     K to J
#     J to E
#     E to D
#     D to I
#
# Afterward, the map of orbits looks like this:
#
#         G - H       J - K - L
#        /           /
# COM - B - C - D - E - F
#                \
#                 I - SAN
#                  \
#                   YOU
#
# What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)


def path(from_node, to_node):
    for w in walk(from_node):
        if w[0] == to_node:
            return w[2]


path_to_you = path("COM", "YOU")
path_to_santa = path("COM", "SAN")

common_start_len = 0
while path_to_you[common_start_len] == path_to_santa[common_start_len]:
    common_start_len += 1

print("Part Two:", len(path_to_you[common_start_len:]) + len(path_to_santa[common_start_len:]) - 2)
