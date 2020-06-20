import unittest
from aoc09.day18 import *


class TestDay18(unittest.TestCase):
    def test_keys(self):
        the_map = [
            "########################",
            "#f.D.E.e.C.b.....@.B.c.#",
            "######################.#",
            "#d.....................#",
            "########################"
        ]
        self.assertEqual("bcdef", all_keys(the_map))

    def test_collect(self):
        m = map_to_matrix([
            "#########",
            "#b.A.@.a#",
            "#########"
        ])
        n = number_of_moves_to_collect_all_keys(m)
        self.assertEqual(n, 8)

    def test_collect_2(self):
        m = map_to_matrix([
            "########################",
            "#f.D.E.e.C.b.A.@.a.B.c.#",
            "######################.#",
            "#d.....................#",
            "########################"
        ])

        n = number_of_moves_to_collect_all_keys(m)
        self.assertEqual(n, 86)

    def test_collect_3(self):
        m = map_to_matrix([
            "########################",
            "#@..............ac.GI.b#",
            "###d#e#f################",
            "###A#B#C################",
            "###g#h#i################",
            "########################"
        ])

        n = number_of_moves_to_collect_all_keys(m)
        self.assertEqual(n, 81)

    def test_collect_4(self):
        m = map_to_matrix([
            "#################",
            "#i.G..c...e..H.p#",
            "########.########",
            "#j.A..b...f..D.o#",
            "########@########",
            "#k.E..a...g..B.n#",
            "########.########",
            "#l.F..d...h..C.m#",
            "#################",
        ])

        n = number_of_moves_to_collect_all_keys(m)
        self.assertEqual(n, 136)
