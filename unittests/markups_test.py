"""
Tests work of markups.py
"""

import unittest

from bot_functions.markups import Markup


class MarkupsTest(unittest.TestCase):
    """
    Tests work of different markups
    """
    def setUp(self) -> None:
        self.markup = Markup()

    def test_change_cur_name(self):
        """
        checks whether markups not empty
        """
        self.assertTrue(len(self.markup.start_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
        self.assertTrue(len(self.markup.income_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
        self.assertTrue(len(self.markup.expense_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
        self.assertTrue(len(self.markup.currency_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
        self.assertTrue(len(self.markup.report_period_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
        self.assertTrue(len(self.markup.report_place_markup()['inline_keyboard']) != 0,
                        'Markup is empty')
