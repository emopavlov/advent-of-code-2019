import unittest
from aoc09.day20 import *


class TestDay20(unittest.TestCase):
    maze1 = [
        "         A           ",
        "         A           ",
        "  #######.#########  ",
        "  #######.........#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #####  B    ###.#  ",
        "BC...##  C    ###.#  ",
        "  ##.##       ###.#  ",
        "  ##...DE  F  ###.#  ",
        "  #####    G  ###.#  ",
        "  #########.#####.#  ",
        "DE..#######...###.#  ",
        "  #.#########.###.#  ",
        "FG..#########.....#  ",
        "  ###########.#####  ",
        "             Z       ",
        "             Z       "
    ]

    def test_portals(self):
        m = Matrix()
        m.init_from_string('\n'.join(TestDay20.maze1))
        ps = portals(m)
        print(ps)

        self.assertTrue(Target(2, 15, "FG") in ps)
        self.assertTrue(Target(13, 16, "ZZ") in ps)
        self.assertTrue(Target(9, 2, "AA") in ps)

    def test_expand(self):
        m = Matrix()
        m.init_from_string('\n'.join(TestDay20.maze1))
        ps = portals(m)

        def test_expand(x, y):
            return expand(m, set(map(lambda t: t.position(), ps)), x, y)

        positions = test_expand(13, 16)
        self.assertEqual(1, len(positions))
        self.assertTrue((13, 15) in positions)

        positions = test_expand(9, 2)
        self.assertEqual(1, len(positions))
        self.assertTrue((9, 3) in positions)

        positions = test_expand(9, 3)
        self.assertEqual(3, len(positions))
        self.assertTrue((9, 2) in positions)
        self.assertTrue((9, 4) in positions)
        self.assertTrue((10, 3) in positions)

        positions = test_expand(2, 15)
        self.assertEqual(1, len(positions))
        self.assertTrue((3, 15) in positions)

    def test_construct_graph(self):
        m = Matrix()
        m.init_from_string('\n'.join(TestDay20.maze1))
        ps = portals(m)

        g = construct_graph(ps, m)

        print(g)

        self.assertEqual(26, g.distance("AA", "ZZ"))
        self.assertEqual(1, g.distance("BC", "BCX"))

    def test_search(self):
        m = Matrix()
        m.init_from_string('\n'.join(TestDay20.maze1))
        ps = portals(m)
        g = construct_graph(ps, m)
        min_distance = dijkstra(g, "AA", "ZZ")
        self.assertEqual(23, min_distance)

    def test_shortest_path(self):
        maze = util.read_input("day20_test_input_2", should_strip=False, folder="../tests/input/")
        m = Matrix()
        m.init_from_string('\n'.join(maze))
        ps = portals(m)

        g = construct_graph(ps, m)
        min_distance = dijkstra(g, "AA", "ZZ")
        self.assertEqual(58, min_distance)
