import unittest
from diplomacy.engine.game import Game

class TestGetUnits(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_one_power(self):
        self.game.clear_units()
        self.game.set_units('FRANCE', ['A PAR', 'A MAR'])
        self.game.set_units('ENGLAND', ['A PAR', 'A LON'])
        units = self.game.get_units("france")
        self.assertEqual(units, ['A MAR'])

    def test_all_powers(self):
        self.game.clear_units()
        self.game.set_units('FRANCE', ['A PAR', 'A MAR'])
        self.game.set_units('ENGLAND', ['A PAR', 'A LON'])

        all_units = self.game.get_units()

        self.assertEqual(all_units['AUSTRIA'], [])
        self.assertEqual(all_units['ENGLAND'], ['A PAR', 'A LON'])
        self.assertEqual(all_units['FRANCE'], ['A MAR'])
        self.assertEqual(all_units['GERMANY'], [])
        self.assertEqual(all_units['ITALY'], [])
        self.assertEqual(all_units['RUSSIA'], [])
        self.assertEqual(all_units['TURKEY'], [])


class TestGetOrders(unittest.TestCase):
    def check_sorted(self, list_1, list_2):
        return sorted(list_1) == sorted(list_2)

    def setUp(self):
        self.game = Game()

    def test_phase_m(self):
        self.game.set_current_phase("S1901M")
        self.game.set_orders('FRANCE', ['A PAR H', 'A MAR - BUR'])
        self.game.set_orders('ENGLAND', ['LON H'])
        orders = self.game.get_orders()

        self.assertTrue(self.check_sorted(orders['ENGLAND'], ['F LON H']))
        self.assertTrue(self.check_sorted(orders['FRANCE'], ['A PAR H', 'A MAR - BUR']))

    def test_phase_a(self):
        self.game.clear_units()
        self.game.set_current_phase("W1901A")
        self.game.set_orders('FRANCE', ['A MAR B', 'F MAR B'])
        self.game.set_orders('AUSTRIA', ['A PAR H'])
        self.game.set_orders('ENGLAND', ['A LON B'])
        orders = self.game.get_orders()

        self.assertTrue(self.check_sorted(orders['ENGLAND'], ['A LON B']))
        self.assertTrue(self.check_sorted(orders['FRANCE'], ['A MAR B']))
        self.assertTrue(self.check_sorted(orders['AUSTRIA'], []))

    def test_no_check_rule(self):
        game = Game()
        game.set_current_phase("S1901M")
        game.add_rule("NO_CHECK")

        # Invalid move
        game.set_orders('FRANCE', ['A PAR - EDI', 'F MAR B'])
        game.set_orders('AUSTRIA', ['A PAR H'])
        orders = game.get_orders()

        self.assertTrue(self.check_sorted(orders['FRANCE'], ['A PAR - EDI', 'F MAR B']))
        self.assertTrue(self.check_sorted(orders['AUSTRIA'], ['A PAR H']))


if __name__ == '__main__':
    unittest.main()
