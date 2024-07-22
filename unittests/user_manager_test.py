"""
Checks send_statistics method
"""
import unittest
import datetime

from database_handling.users_manager import UsersManager
from database.db import BotDB


class TestStatistics(unittest.TestCase):
    """
        Tests the work of statistics
    """

    def setUp(self) -> None:
        self.bot = BotDB()
        self.user = UsersManager()
        self.user_id = 101
        self.cat = '📈 Зарплата'
        self.value = float(60)
        self.cur = '₽'
        self.within = 'day'

    def test_statistics(self):
        """
            Checks the sent statistic
        """
        date = datetime.datetime.now().strftime("%A").upper()
        try:
            self.user.register_user(user_id=self.user_id)
            self.bot.add_record(user_id=self.user_id, category=self.cat,
                                operation=1, value=self.value)

        except AssertionError:
            self.bot.delete_history(user_id=self.user_id)

        exp = f"<u>Доходы {date}</u>:\n{self.cat}: {self.value} {self.cur}\n---\n<b>Итого:</b>" \
                   f" {self.value} {self.cur}\n\n" \
                   f"<u>Расходы {date}</u>:\n---\n<b>Итого:</b> {0} {self.cur}"

        actual = self.user.show_statistics(self.user_id, self.within)
        self.assertEqual(exp, actual)

    def test_statistics_wrong(self):
        """
            Checks when there are no statistics
        """
        self.bot.delete_history(user_id=self.user_id)

        expected = "У Вас нет записей о доходах и расходах"
        actual = self.user.show_statistics(self.user_id, self.within)

        self.assertEqual(expected, actual)
