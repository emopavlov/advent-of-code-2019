import unittest
from aoc09.tools.robot import EmergencyHullPaintingRobot
from aoc09.tools.incode_computer import IntcodeComputer

empty_computer = IntcodeComputer([99])
black = "."
white = "#"


class TestEmergencyHullPaintingRobot(unittest.TestCase):

    def test_read_colour(self):
        robot = EmergencyHullPaintingRobot(empty_computer)
        self.assertEqual(black, robot._read_colour())

    def test_paint_and_move(self):
        robot = EmergencyHullPaintingRobot(empty_computer)
        commands = [(1, 0), (0, 1)]
        for (c, t) in commands:
            robot._paint_and_move(c, t)

        self.assertEqual(robot.hull.path, {(0, 0): white, (-1, 0): black})
