import unittest
from aoc09.tools import compression


class TestCompression(unittest.TestCase):

    def test_split_sequence(self):
        test_sequence = "R,8,L,8,R,8,L,12,L,8".split(",")

        # leading match
        result = compression.replace_all(test_sequence, ['R', '8'], ':')
        self.assertEqual([[':'], ['L', '8'], [':'], ['L', '12', 'L', '8']], result)

        # trailing match
        result = compression.replace_all(test_sequence, ['L', '8'], ':')
        self.assertEqual([['R', '8'], [':'], ['R', '8', 'L', '12'], [':']], result)

        # middle match
        result = compression.replace_all(test_sequence, ['8', 'R', '8'], ':')
        self.assertEqual([['R', '8', 'L'], [':'], ['L', '12', 'L', '8']], result)

    def test_sequence_compare(self):
        test_sequence = "R,8,L,8,R,8,L,12,L,8".split(",")

        self.assertTrue(compression.sequence_compare(['R', '8', 'L'], test_sequence, 0))
        self.assertTrue(compression.sequence_compare(['L', '8'], test_sequence, 8))
        self.assertTrue(compression.sequence_compare(['8', 'L'], test_sequence, 1))
        self.assertFalse(compression.sequence_compare(['8', 'L'], test_sequence, 2))
        self.assertFalse(compression.sequence_compare(['L', '8', 'R'], test_sequence, 8))

    def test_replace(self):
        test_sequence_1 = "R,8,L,8,R,8,L,12,L,8".split(",")
        test_sequence_2 = "R,8,L,8,L,8".split(",")

        result = compression.replace([test_sequence_1, test_sequence_2], ['L', '8'], ':')
        self.assertEqual(result, [['R', '8'], [':'], ['R', '8', 'L', '12'], [':'], ['R', '8'], [':'], [':']])

        result = compression.replace([test_sequence_1, test_sequence_2], ['R', '8'], ':')
        self.assertEqual(result, [[':'],  ['L', '8'], [':'], ['L', '12', 'L', '8'], [':'], ['L', '8', 'L', '8']])

    def test_compress(self):
        test_sequence_1 = "R,8,R,8,R,4,R,4,R,8,L,6,L,2,R,4,R,4,R,8,R,8,R,8,L,6,L,2".split(",")
        compression.compress([test_sequence_1], 3, 6, [])
