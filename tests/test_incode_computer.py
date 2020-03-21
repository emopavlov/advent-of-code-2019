import unittest
from aoc09 import incode_computer


class TestIntcodeComputer(unittest.TestCase):

    # 1 - add
    def test_addition(self):
        comp = incode_computer.IntcodeComputer([1, 0, 0, 3, 99])
        comp.run()
        self.assertEqual([1, 0, 0, 2, 99], comp.memory.dump())

        # immediate mode addition
        comp = incode_computer.IntcodeComputer([1002, 4, 3, 4, 33])
        comp.run()
        self.assertEqual([1002, 4, 3, 4, 99], comp.memory.dump())

        # immediate mode addition
        comp = incode_computer.IntcodeComputer([1101, 100, -1, 4, 0])
        comp.run()
        self.assertEqual([1101, 100, -1, 4, 99], comp.memory.dump())

    # 2 - multi
    def test_multiplication(self):
        comp = incode_computer.IntcodeComputer([2, 3, 0, 3, 99])
        comp.run()
        self.assertEqual([2, 3, 0, 6, 99], comp.memory.dump())

    # 3/4 - read/write
    def test_input_output(self):
        # out the input
        comp = incode_computer.IntcodeComputer([3, 0, 4, 0, 99])
        comp.run([17])
        self.assertEqual([17], comp.output_list)

        # write relative param
        comp = incode_computer.IntcodeComputer([109, 15, 204, -11, 99])
        comp.run()
        self.assertEqual([99], comp.output_list)

        # read relative param
        comp = incode_computer.IntcodeComputer([109, 15, 203, -10, 104, 0, 99])
        comp.run([33])
        self.assertEqual([33], comp.output_list)

    def test_jump(self):
        comp = incode_computer.IntcodeComputer([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
        comp.run([0])
        self.assertEqual([0], comp.output_list)

        # immediate mode
        comp = incode_computer.IntcodeComputer([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
        comp.run([8484734])
        self.assertEqual([1], comp.output_list)

    def test_equlas(self):
        comp = incode_computer.IntcodeComputer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
        comp.run([8])
        self.assertEqual([1], comp.output_list)

        comp = incode_computer.IntcodeComputer([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
        comp.run([7])
        self.assertEqual([0], comp.output_list)

        comp = incode_computer.IntcodeComputer([3, 3, 1108, -1, 8, 3, 4, 3, 99])
        comp.run([18])
        self.assertEqual([0], comp.output_list)

        comp = incode_computer.IntcodeComputer([3, 3, 1108, -1, 8, 3, 4, 3, 99])
        comp.run([8])
        self.assertEqual([1], comp.output_list)

    def test_immediate_mode(self):
        # immediate mode addition
        comp = incode_computer.IntcodeComputer([1002, 4, 3, 4, 33])
        comp.run()
        self.assertEqual([1002, 4, 3, 4, 99], comp.memory.dump())

        # immediate mode addition
        comp = incode_computer.IntcodeComputer([1101, 100, -1, 4, 0])
        comp.run()
        self.assertEqual([1101, 100, -1, 4, 99], comp.memory.dump())

    def test_relative_mode(self):
        # add to relative base
        mem = [109, 19, 99]
        comp = incode_computer.IntcodeComputer(mem.copy())
        comp.relative_base = 2000
        comp.run()
        self.assertEqual(2019, comp.relative_base)

        # subtract from relative base
        mem = [109, -19, 99]
        comp = incode_computer.IntcodeComputer(mem.copy())
        comp.relative_base = 2000
        comp.run()
        self.assertEqual(1981, comp.relative_base)

        # returns a copy of itself
        mem = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        comp = incode_computer.IntcodeComputer(mem.copy())
        comp.run()
        self.assertEqual(mem, comp.output_list)

    def test_large_numbers(self):
        # number with 16 digits
        comp = incode_computer.IntcodeComputer([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
        comp.run()
        self.assertTrue(10000000000000000 > comp.output_list[0] > 999999999999999, f"result was #{comp.output_list[0]}")

        # output the large number
        comp = incode_computer.IntcodeComputer([104, 1125899906842624, 99])
        comp.run()
        self.assertEqual(1125899906842624, comp.output_list[0])
