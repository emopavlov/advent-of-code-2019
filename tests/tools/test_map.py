import unittest
from aoc09.tools.map import Map, Location


class TestMap(unittest.TestCase):

    def test_map_set(self):
        print("running test")
        m = Map()
        m.set(1, 2, "x")
        m.set(2, 2, "x")
        m.set(2, 1, ".")

        m.print()
        self.assertEqual("x", m.get(2, 2))
