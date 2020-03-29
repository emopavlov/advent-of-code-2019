import unittest
from aoc09.day12 import FlatPlanetarySystem, PlanetarySystem, Planet, lcm


class TestDay12(unittest.TestCase):

    def test_planet(self):
        p = Planet((12, 0, -12))
        p.velocity = (4, -2, 7)
        self.assertEqual(24, p.e_potential())
        self.assertEqual(13, p.e_kinetic())
        self.assertEqual(312, p.e_total())

    def test_delta(self):
        tuples = [(1, 2, 3), (0, 3, -7), (12, 0, -12)]
        self.assertEqual((2, 2, -1), PlanetarySystem.delta(tuples, (0, 0, 0)))

        tuples = [(1, 2, 3), (0, 3, -7), (12, 0, -12)]
        self.assertEqual((-1, -3, -3), PlanetarySystem.delta(tuples, (3, 4, 8)))

        tuples = [(1, 2, 3), (0, 3, -7), (12, 0, -12), (20, 55, 1)]
        self.assertEqual((0, -2, -4), PlanetarySystem.delta(tuples, (3, 4, 8)))

    def test_tick(self):
        start = [
            Planet((1, 2, 3)),
            Planet((0, 3, -7)),
            Planet((12, 0, -12))
        ]
        ps = PlanetarySystem(start)

        # No velocity yet, nothing should happen
        ps.update_positions()
        self.assertEqual(start, ps.planets)

        ps.update_velocities()
        self.assertEqual([(0, 0, -2), (2, -2, 0), (-2, 2, 2)], list(map(lambda x: x.velocity, ps.planets)))
        ps.update_positions()
        self.assertEqual([(1, 2, 1), (2, 1, -7), (10, 2, -10)], list(map(lambda x: x.position, ps.planets)))

        start = [
            Planet((1, 2, 3)),
            Planet((0, 3, -7)),
            Planet((12, 0, -12))
        ]
        ps2 = PlanetarySystem(start)
        ps2.tick()
        self.assertEqual([(0, 0, -2), (2, -2, 0), (-2, 2, 2)], list(map(lambda x: x.velocity, ps2.planets)))
        self.assertEqual([(1, 2, 1), (2, 1, -7), (10, 2, -10)], list(map(lambda x: x.position, ps2.planets)))

    def test_simulate(self):
        planets = [Planet((-1, 0, 2)), Planet((2, -10, -7)), Planet((4, -8, 8)), Planet((3, 5, -1))]
        ps = PlanetarySystem(planets)
        ps.simulate(10)
        self.assertEqual(10, ps.time)
        self.assertEqual([(-3, -2, 1), (-1, 1, 3), (3, 2, -3), (1, -1, -1)], list(map(lambda x: x.velocity, ps.planets)))
        self.assertEqual([(2, 1, -3), (1, -8, 0), (3, -6, 1), (2, 0, 4)], list(map(lambda x: x.position, ps.planets)))
        self.assertEqual(179, ps.energy())

    # Part two
    def test_delta_2(self):
        d = FlatPlanetarySystem.delta((14, 7, -3, 0, 13), 5)
        self.assertEqual(1, d)

    def test_update_velocities_2(self):
        start = [
            Planet((1, 2, 3)),
            Planet((0, 3, -7)),
            Planet((12, 0, -12))
        ]
        ps = FlatPlanetarySystem(start, 1)
        ps.update_velocities()
        self.assertEqual([0, -2, 2], ps.velocities)

        ps = FlatPlanetarySystem(start, 2)
        ps.update_velocities()
        self.assertEqual([-2, 0, 2], ps.velocities)

        ps = FlatPlanetarySystem(start, 0)
        ps.update_velocities()
        self.assertEqual([0, 2, -2], ps.velocities)

    def test_tick_2(self):
        start = [
            Planet((1, 2, 3)),
            Planet((0, 3, -7)),
            Planet((12, 0, -12))
        ]
        ps = FlatPlanetarySystem(start, 1)
        ps.tick()
        self.assertEqual([0, -2, 2], ps.velocities)
        self.assertEqual([2, 1, 2], ps.positions)

        ps = FlatPlanetarySystem(start, 2)
        ps.tick()
        self.assertEqual([-2, 0, 2], ps.velocities)
        self.assertEqual([1, -7, -10], ps.positions)

        ps = FlatPlanetarySystem(start, 0)
        ps.tick()
        self.assertEqual([0, 2, -2], ps.velocities)
        self.assertEqual([1, 2, 10], ps.positions)

    def test_lcm(self):
        self.assertEqual(96, lcm(8, 32, 48))

    def test_simulation_2(self):
        planets = [Planet((-1, 0, 2)), Planet((2, -10, -7)), Planet((4, -8, 8)), Planet((3, 5, -1))]
        ps = FlatPlanetarySystem(planets, 0)
        ps.simulate_cycle()
        steps_1 = ps.time

        ps = FlatPlanetarySystem(planets, 1)
        ps.simulate_cycle()
        steps_2 = ps.time

        ps = FlatPlanetarySystem(planets, 2)
        ps.simulate_cycle()
        steps_3 = ps.time
        self.assertEqual(2772, lcm(steps_1, steps_2, steps_3))

        # second example
        planets = [Planet((-8, -10, 0)), Planet((5, 5, 10)), Planet((2, -7, 3)), Planet((9, -8, -3))]
        ps = FlatPlanetarySystem(planets, 0)
        ps.simulate_cycle()
        steps_1 = ps.time

        ps = FlatPlanetarySystem(planets, 1)
        ps.simulate_cycle()
        steps_2 = ps.time

        ps = FlatPlanetarySystem(planets, 2)
        ps.simulate_cycle()
        steps_3 = ps.time
        self.assertEqual(4686774924, lcm(steps_1, steps_2, steps_3))
