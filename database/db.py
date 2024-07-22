"""
Works with database
"""
import sqlite3

from auxiliary_files.constants import PROJECT_ROOT


class BotDB:
    """
    Creates database
    """
    def __init__(self):
        self.conn = sqlite3.connect(PROJECT_ROOT / "accountant.db")
        self.cursor = self.conn.cursor()

    def create_users_table(self):
        """
        Creates a table with users data
        """
        self.cursor.executescript("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        currency TEXT DEFAULT ₽ NOT NULL,
        join_date DATETIME DEFAULT (DATETIME('now')) NOT NULL);
        """)
        self.conn.commit()

    def create_records_table(self):
        """
        Creates a table with users' records
        """
        self.cursor.executescript("""CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        users_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
        category TEXT NOT NULL,
        operation BOOLEAN NOT NULL,
        value DECIMAL NOT NULL,
        date DATETIME DEFAULT (DATETIME('now')) NOT NULL);
        """)
        self.conn.commit()

    def user_exists(self, user_id):
        """
        Checks whether a user exists in the table
        """
        with self.conn:
            return bool(self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?",
                                            (user_id,)).fetchall())

    def add_user(self, user_id, currency='₽'):
        """
        Adds a new user
        """
        with self.conn:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `currency`) VALUES (?, ?)",
                                       (user_id, currency))

    def get_currency(self, user_id):
        """
        Selects currency
        """
        with self.conn:
            return self.cursor.execute("SELECT `currency` FROM `users` WHERE `user_id` = ?",
                                       (user_id,)).fetchone()[0]

    def get_id(self, user_id):
        """
        Creates another id to connect two tables
        """
        with self.conn:
            return self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?",
                                       (user_id,)).fetchone()[0]

    def add_record(self, user_id, category, operation, value):
        """
        Adds record to table 'records'
        """
        self.cursor.execute("""INSERT INTO `records` (
        `users_id`, `category`, `operation`, `value`
        )
        VALUES (?, ?, ?, ?)""",
                            (self.get_id(user_id),
                             category,
                             operation,
                             value))
        return self.conn.commit()

    def change_currency(self, user_id, new_cur, coef):
        """
        Changes currency the user has chosen
        """
        self.cursor.execute("UPDATE `users` SET `currency` = ? WHERE `user_id` = ?",
                            (new_cur, user_id))
        self.cursor.execute("UPDATE `records` SET `value` = `value` * ? WHERE `users_id` = ?",
                            (coef, self.get_id(user_id)))
        return self.conn.commit()

    def get_inc_exp(self, user_id, operation, within="all"):
        """
        Gets incomes and expenses from table 'records'
        """
        if within == "day":
            result = self.cursor.execute(
                "SELECT `category`, `value`, `date` FROM `records` WHERE `users_id` = ? "
                "AND `operation` = ? "
                "AND `date` BETWEEN datetime('now', 'start of day') "
                "AND datetime('now', 'localtime') "
                "ORDER BY `date` DESC",
                (self.get_id(user_id), operation)).fetchall()
        elif within == "week":
            result = self.cursor.execute(
                "SELECT `category`, `value`, `date` FROM `records` WHERE `users_id` = ? "
                "AND `operation` = ? "
                "AND `date` BETWEEN datetime('now', '-6 days') "
                "AND datetime('now', 'localtime') "
                "ORDER BY `date` DESC",
                (self.get_id(user_id), operation)).fetchall()
        elif within == "month":
            result = self.cursor.execute(
                "SELECT `category`, `value`, `date` FROM `records` WHERE `users_id` = ? "
                "AND `operation` = ? "
                "AND `date` BETWEEN datetime('now', 'start of month') "
                "AND datetime('now', 'localtime') "
                "ORDER BY `date` DESC",
                (self.get_id(user_id), operation)).fetchall()
        elif within == "year":
            result = self.cursor.execute(
                "SELECT `category`, `value`, `date` FROM `records` WHERE `users_id` = ? "
                "AND `operation` = ? "
                "AND `date` BETWEEN datetime('now', 'start of year') "
                "AND datetime('now', 'localtime') "
                "ORDER BY `date` DESC",
                (self.get_id(user_id), operation)).fetchall()
        else:
            result = self.cursor.execute(
                "SELECT `category`, `value`, `date` FROM `records` WHERE `users_id` = ? "
                "AND `operation` = ? "
                "ORDER BY `date` DESC",
                (self.get_id(user_id), operation)).fetchall()
        return result

    def delete_history(self, user_id):
        """
        Deletes all the records about user's incomes and expenses from table 'records'
        """
        self.cursor.execute("DELETE FROM `records` WHERE `users_id` = ?",
                            (self.get_id(user_id),))
        self.conn.commit()

    def close(self):
        """
        Closes database
        """
        self.conn.close()
