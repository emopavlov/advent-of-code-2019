import unittest
from aoc09.day10 import *


class TestDay10(unittest.TestCase):

    def test_spiral_search(self):
        asteroid_map = (
            "1239G",
            "804AH",
            "765BI",
            "FEDCJ",
            "ONMLK"
        )

        output = []
        m = to_matrix(asteroid_map)
        spiral_search(output.append, m, (1, 1))
        self.assertEqual(
            output,
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
             "M", "N", "O"]
        )

    def test_check_visible_vertical(self):
        asteroid_map = (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"
        )

        m = to_matrix(asteroid_map)
        hidden = find_hidden((4, 3), (4, 2), m)
        self.assertEqual([(4, 0)], hidden)

    def test_check_visible(self):
        asteroid_map = (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"
        )

        m = to_matrix(asteroid_map)
        hidden = find_hidden((1, 0), (2, 2), m)
        self.assertEqual([(3, 4)], hidden)

        hidden = find_hidden((3, 4), (2, 2), m)
        self.assertEqual([(1, 0)], hidden)

        hidden = find_hidden((4, 3), (3, 2), m)
        self.assertEqual([(1, 0)], hidden)

        hidden = find_hidden((4, 3), (2, 2), m)
        self.assertEqual([], hidden)

        # going left
        hidden = find_hidden((1, 2), (2, 2), m)
        self.assertEqual([(3, 2), (4, 2)], hidden)

        # going right
        hidden = find_hidden((2, 2), (1, 2), m)
        self.assertEqual([(0, 2)], hidden)

    # best (3,4) with 8
    def test_asteroid_visibility(self):
        asteroid_map = (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"
        )

        m = to_matrix(asteroid_map)
        self.assertEqual(8, visible_asteroids_count((3, 4), m))
        self.assertEqual(7, visible_asteroids_count((2, 2), m))
        self.assertEqual(7, visible_asteroids_count((4, 3), m))

    # best (3,4) with 8
    def test_asteroid_with_best_visibility(self):
        asteroid_map = (
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"
        )

        m = to_matrix(asteroid_map)
        self.assertEqual(((3, 4), 8), asteroid_with_best_visibility(m))

    def test_sort_points(self):
        points = [(10, 10), (5, 7), (0, 2), (-1, -4), (2, 0), (-4, 0), (0, -17), (5, 6), (-2, -4), (3, -5)]
        self.assertEqual(
            [(0, -17), (3, -5), (2, 0),(10, 10), (5, 6), (5, 7), (0, 2), (-4, 0), (-2, -4), (-1, -4)],
            sort_points(points)
        )

    def test_find_n_destroyed_asteroid(self):
        asteroid_map = (
            ".#....#####...#..",
            "##...##.#####..##",
            "##...#...#.#####.",
            "..#.....X...###..",
            "..#.#.....#....##",
        )

        m = to_matrix(asteroid_map)
        self.assertEqual((14, 3), find_n_destroyed_asteroid(m, (8, 3), 36))
        self.assertEqual((2, 4), find_n_destroyed_asteroid(m, (8, 3), 19))
        self.assertEqual((9, 2), find_n_destroyed_asteroid(m, (8, 3), 5))

