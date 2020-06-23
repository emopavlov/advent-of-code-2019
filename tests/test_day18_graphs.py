import unittest
from aoc09.day18_graphs import *


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

    def test_paths(self):
        m = map_to_matrix([
            "#########",
            "#b.A.@.a#",
            "#########"
        ])
        paths = find_edges(m, "@", {"a", "b"})
        print(paths)

    def test_paths_2(self):
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
        paths = find_edges(m, "@", all_keys(m.values))
        print(paths)
        # some checks

    def test_build_graph(self):
        m = map_to_matrix([
            "########################",
            "#@..............ac.GI.b#",
            "###d#e#f################",
            "###A#B#C################",
            "###g#h#i################",
            "########################"
        ])
        g = map_to_graph(m)
        # some checks, the graph covers only "shortest" distances but not all paths

    def test_priority_queue(self):
        q = PriorityQueue()
        w1 = ("a", "hgu")
        w2 = ("b", "a")
        w3 = ("g", "")
        q.put((38, w1))
        q.put((7, w3))
        q.put((22, w2))
        self.assertEqual((7, w3), q.get())
        self.assertEqual((22, w2), q.get())
        self.assertEqual((38, w1), q.get())
        self.assertTrue(q.empty())

    def test_expand_walker(self):
        m = map_to_matrix([
            "########################",
            "#@..............ac.GI.b#",
            "###d#e#f################",
            "###A#B#C################",
            "###g#h#i################",
            "########################"
        ])
        g = map_to_graph(m)
        w = ("a", "@a")
        print(expand_walker(w, g))

    def test_collect(self):
        m = map_to_matrix([
            "#########",
            "#b.A.@.a#",
            "#########"
        ])
        g = map_to_graph(m)
        n = walk_graph(g, "@")
        self.assertEqual(n, 8)

    def test_collect_2(self):
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
        g = map_to_graph(m)
        n = walk_graph(g, "@")
        self.assertEqual(n, 136)
