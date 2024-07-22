"""
Tests work of currency_converter.py
"""

import unittest

from bot_functions.currency_converter import CurrencyConverter


class CurrencyConverterTest(unittest.TestCase):
    """
    Tests work of currency_converter.py
    """
    def setUp(self) -> None:
        self.cur_con = CurrencyConverter(old_cur='₽')

    def test_change_cur_name(self):
        """
        Tests whether change_cur_name function takes only specific values
        """
        trash = [1, 1.1, 'RUB', [], {}, (), True, None]
        with self.assertRaises(KeyError):
            for i in trash:
                self.cur_con = CurrencyConverter(old_cur=i)
                self.cur_con.change_cur_name()

    def test_get_coef(self):
        """
        Tests whether get_coef function returns float
        """
        self.assertTrue(isinstance(self.cur_con.get_coef("$"), float))
