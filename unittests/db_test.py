"""
Checks work of db.py
"""

import unittest
import os

from datetime import datetime

from auxiliary_files.constants import PROJECT_ROOT
from database.db import BotDB


class DatabaseTest(unittest.TestCase):
    """
    Checks work of db.py
    """
    def setUp(self) -> None:
        self.d_b = BotDB()

    def test_db_existence(self):
        """
        Checks the existence of 'accountant.db' database in the directory
        """
        self.assertEqual('accountant.db' in os.listdir(PROJECT_ROOT), True,
                         'no database "accountant.db" in the directory')

    def test_db_connection(self):
        """
        Tests connection to the database
        """
        self.assertEqual(self.d_b.conn is not None, True, 'no connection to database')

    def test_users_creation(self):
        """
        Tests creation of table 'users' in the database
        """
        with open(
                PROJECT_ROOT / 'unittests' / 'test_users_table_creation.sql',
                encoding='utf-8') as file:
            query = file.read()
        self.d_b.cursor.executescript(query)
        actual = self.d_b.cursor.execute("SELECT * FROM `users`").fetchall()
        expected = [(1, 123456789, "$", "2022-01-01 01:01:01")]
        self.assertEqual(actual, expected)

    def test_records_creation(self):
        """
        Tests creation of table 'records' in the database
        """
        with open(PROJECT_ROOT / 'unittests' / 'test_records_table_creation.sql',
                  encoding='utf-8') as file:
            query = file.read()
        self.d_b.cursor.executescript(query)
        actual = self.d_b.cursor.execute("SELECT * FROM `records`").fetchall()
        expected = [(1, 1, '📚 Education', 1, 10000, '2022-01-01 01:01:01')]
        self.assertEqual(actual, expected)

    def test_users_format(self):
        """
        Checks whether columns in table 'users' have appropriate types
        """
        users_info = self.d_b.cursor.execute("SELECT * FROM `users`").fetchall()
        for u_i in users_info:
            self.assertTrue(isinstance(u_i[0], int))
            self.assertTrue(isinstance(u_i[1], int))
            self.assertTrue(u_i[2] in ["₽", "$", "€"])
            self.assertTrue(isinstance(u_i[3], str)
                            and datetime.strptime(u_i[3], '%Y-%m-%d %H:%M:%S'))

    def test_records_format(self):
        """
        Checks whether columns in table 'records' have appropriate types
        """
        records_info = self.d_b.cursor.execute("SELECT * FROM `records`").fetchall()
        for r_i in records_info:
            self.assertTrue(isinstance(r_i[0], int))
            self.assertTrue(isinstance(r_i[1], int))
            self.assertTrue(isinstance(r_i[2], str))
            self.assertTrue(r_i[3] in [1, -1])
            self.assertTrue(isinstance(r_i[4], int))
            self.assertTrue(isinstance(r_i[5], str)
                            and datetime.strptime(r_i[5], '%Y-%m-%d %H:%M:%S'))

    def test_history_deletion(self):
        """
        Checks whether all records from current user are deleted
        """
        with open(
                PROJECT_ROOT / 'unittests' / 'test_records_table_creation.sql',
                encoding='utf-8') as file:
            query = file.read()
        self.d_b.cursor.executescript(query)
        self.d_b.delete_history(123456789)
        self.assertEqual(
            self.d_b.cursor.execute(
                "SELECT * from `records` WHERE users_id = 123456789"
            ).fetchall(), [])
