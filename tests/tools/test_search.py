import unittest
import string
from aoc09.tools.matrix import Matrix
from aoc09.tools.search import *


class TestSearch(unittest.TestCase):

    def test_bfs_to_graph(self):
        the_map = [
            "########################",
            "#f.D.E.e.C.b.....@.B.c.#",
            "######################.#",
            "#d.....................#",
            "########################"
        ]
        m = Matrix()
        targets = []
        m.init_from_string('\n'.join(the_map))
        for x, y in m.index_range():
            name = m.get(x, y)
            if name in string.ascii_lowercase:
                targets.append(Target(x, y, name))

        def expand(x, y):
            x_expand = list(map(lambda x: (x, y), filter(lambda x: x >= 0 and x < m.width, [x + 1, x - 1])))
            y_expand = list(map(lambda y: (x, y), filter(lambda x: x >= 0 and x < m.height, [y + 1, y - 1])))
            return list(filter(lambda p: m.get(*p) != "#", x_expand + y_expand))

        g = bfs_to_graph(targets, expand)

        self.assertEqual(10, g.distance('b', 'c'))
        self.assertEqual(44, g.distance('d', 'f'))
        self.assertEqual(len(targets), len(g.__neighbours))
