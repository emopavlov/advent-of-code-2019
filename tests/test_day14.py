import unittest
from aoc09.day14 import Expression, Compound, Definition, read_definitions, definition_tiers
from math import floor


class TestDay14(unittest.TestCase):
    def test_replace(self):
        definitions = {"A": Definition([Compound("ORE", 5)], Compound("A", 1))}
        result = Expression._replace(Compound("A", 3), definitions)
        self.assertEqual([Compound("ORE", 15)], result)

        definitions = {"B": Definition([Compound("ORE", 8)], Compound("B", 3))}
        result = Expression._replace(Compound("B", 23), definitions)
        self.assertEqual([Compound("ORE", 64)], result)

    def test_group_by_chemical(self):
        results = Expression._group_by_chemical([Compound("ORE", 2), Compound("A", 3), Compound("ORE", 1)])
        expected = [[Compound("A", 3)], [Compound("ORE", 2), Compound("ORE", 1)]]
        for r in results:
            expected.remove(r)
        self.assertTrue(expected == [], f"Does not match expected: {results}")

    def test_sum(self):
        grouped = [[Compound("A", 3)], [Compound("ORE", 2), Compound("ORE", 1)]]
        summed = Expression._sum(grouped)
        self.assertEqual([Compound("A", 3), Compound("ORE", 3)], summed)

    def test_expression(self):
        definitions = {"A": Definition([Compound("ORE", 5)], Compound("A", 1))}
        tiers = definition_tiers(definitions)
        exp = Expression(definitions, tiers, [Compound("A", 2)])
        exp.reduce(definitions)
        self.assertEqual([Compound("ORE", 10)], exp.compounds)

    def test_definition_tiers(self):
        defs = (
            "9 ORE => 2 A",
            "8 ORE => 3 B",
            "7 ORE => 5 C",
            "3 A, 4 B => 1 AB",
            "5 B, 7 C => 1 BC",
            "4 C, 1 A => 1 CA",
            "2 AB, 3 BC, 4 CA => 1 FUEL"
        )

        tiers = definition_tiers(read_definitions(list(defs)))
        self.assertEqual([['ORE'], ['A', 'B', 'C'], ['AB', 'BC', 'CA'], ['FUEL']], tiers)

    def test_to_ore(self):
        defs = (
            "9 ORE => 2 A",
            "8 ORE => 3 B",
            "7 ORE => 5 C",
            "3 A, 4 B => 1 AB",
            "5 B, 7 C => 1 BC",
            "4 C, 1 A => 1 CA",
            "2 AB, 3 BC, 4 CA => 1 FUEL"
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(165, e.compounds[0].quantity)

    def test_to_ore_2(self):
        defs = (
            "157 ORE => 5 NZVS",
            "165 ORE => 6 DCFZ",
            "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
            "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
            "179 ORE => 7 PSHF",
            "177 ORE => 5 HKGWZ",
            "7 DCFZ, 7 PSHF => 2 XJWVT",
            "165 ORE => 2 GPVTF",
            "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(13312, e.compounds[0].quantity)

    def test_to_ore_3(self):
        defs = (
            "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
            "17 NVRVD, 3 JNWZP => 8 VPVL",
            "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
            "22 VJHF, 37 MNCFX => 5 FWMGM",
            "139 ORE => 4 NVRVD",
            "144 ORE => 7 JNWZP",
            "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
            "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
            "145 ORE => 6 MNCFX",
            "1 NVRVD => 8 CXFTF",
            "1 VJHF, 6 MNCFX => 4 RFSQX",
            "176 ORE => 6 VJHF",
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(180697, e.compounds[0].quantity)

    def test_to_ore_4(self):
        defs = (
            "171 ORE => 8 CNZTR",
            "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
            "114 ORE => 4 BHXH",
            "14 VRPVC => 6 BMBT",
            "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
            "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
            "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
            "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
            "5 BMBT => 4 WPTQ",
            "189 ORE => 9 KTJDG",
            "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
            "12 VRPVC, 27 CNZTR => 2 XDBXC",
            "15 KTJDG, 12 BHXH => 5 XCVML",
            "3 BHXH, 2 VRPVC => 7 MZWV",
            "121 ORE => 7 VRPVC",
            "7 XCVML => 6 RJRHP",
            "5 BHXH, 4 VRPVC => 5 LTCX"
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(2210736, e.compounds[0].quantity)

    def test_to_ore_5(self):
        defs = (
            "157 ORE => 5 NZVS",
            "165 ORE => 6 DCFZ",
            "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
            "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
            "179 ORE => 7 PSHF",
            "177 ORE => 5 HKGWZ",
            "7 DCFZ, 7 PSHF => 2 XJWVT",
            "165 ORE => 2 GPVTF",
            "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression.exact_expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(82892753, floor(1000000000000 / e.compounds[0].quantity))

    def test_to_ore_6(self):
        defs = (
            "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
            "17 NVRVD, 3 JNWZP => 8 VPVL",
            "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
            "22 VJHF, 37 MNCFX => 5 FWMGM",
            "139 ORE => 4 NVRVD",
            "144 ORE => 7 JNWZP",
            "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
            "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
            "145 ORE => 6 MNCFX",
            "1 NVRVD => 8 CXFTF",
            "1 VJHF, 6 MNCFX => 4 RFSQX",
            "176 ORE => 6 VJHF",
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression.exact_expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(5586022, floor(1000000000000 / e.compounds[0].quantity))

    def test_to_ore_7(self):
        defs = (
            "171 ORE => 8 CNZTR",
            "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
            "114 ORE => 4 BHXH",
            "14 VRPVC => 6 BMBT",
            "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
            "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
            "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
            "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
            "5 BMBT => 4 WPTQ",
            "189 ORE => 9 KTJDG",
            "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
            "12 VRPVC, 27 CNZTR => 2 XDBXC",
            "15 KTJDG, 12 BHXH => 5 XCVML",
            "3 BHXH, 2 VRPVC => 7 MZWV",
            "121 ORE => 7 VRPVC",
            "7 XCVML => 6 RJRHP",
            "5 BHXH, 4 VRPVC => 5 LTCX"
        )

        definitions = read_definitions(list(defs))
        tiers = definition_tiers(definitions)
        e = Expression.exact_expression(definitions, tiers, [Compound("FUEL", 1)])
        e.to_ore()

        self.assertEqual(1, len(e.compounds))  # only ore
        self.assertEqual(460664, floor(1000000000000 / e.compounds[0].quantity))
