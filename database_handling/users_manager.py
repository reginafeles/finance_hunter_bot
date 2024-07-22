"""
Works with user data
"""
import datetime
from datetime import datetime, timedelta


from database.db import BotDB


class UsersManager:
    """
    For user data
    """

    def __init__(self):
        self.d_b = BotDB()

    def register_user(self, user_id):
        """
        Add a user to database
        """
        if not self.d_b.user_exists(user_id=user_id):
            self.d_b.add_user(user_id=user_id)

    def get_user_cur(self, user_id):
        """
        Extract the user's currency choice from the database
        """
        return self.d_b.get_currency(user_id)

    def add_user_record(self, user_id, category, operation, value):
        """
        Add an operation of the user
        """
        return self.d_b.add_record(user_id=user_id, category=category,
                                   operation=operation, value=value)

    def change_user_currency(self, user_id, new_cur, coef):
        """
        Change the user's currency choice in the database
        """
        return self.d_b.change_currency(user_id=user_id, new_cur=new_cur, coef=coef)

    def text_pattern(self, user_id, user_records):
        """
        Creates a string from the database
        """
        rec_str = ""
        for rec in user_records:
            rec_str += f'{rec[0]}: {round(float(rec[1]), 2)} {self.get_user_cur(user_id=user_id)}\n'
        return rec_str

    @staticmethod
    def date_pattern(date, within):
        """
        Extracts the required timeframe from the current date
        """
        date_pattern = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if within == 'day':
            date = date_pattern.strftime('%A').upper()
        elif within == 'week':
            start = date_pattern - timedelta(days=date_pattern.weekday())
            end = start + timedelta(days=6)
            start = start.strftime('%d-%m')
            end = end.strftime('%d-%m')
            date = f'{start} — {end}'
        elif within == 'month':
            date = date_pattern.strftime('%B %Y').upper()
        elif within == 'year':
            date = date_pattern.strftime('%Y год')
        elif within == 'all':
            date = "за всё время"
        return date

    def show_statistics(self, user_id, within):
        """
        Presents statistics to user
        """
        user_inc = self.d_b.get_inc_exp(user_id=user_id, operation=1, within='all')
        user_exp = self.d_b.get_inc_exp(user_id=user_id, operation=-1, within='all')
        if not user_inc and not user_exp:
            pattern = "У Вас нет записей о доходах и расходах"
        else:
            inc_rep = self.text_pattern(user_id=user_id, user_records=user_inc)
            exp_rep = self.text_pattern(user_id=user_id, user_records=user_exp)
            cur = self.get_user_cur(user_id=user_id)
            sum_inc = round(sum(float(i[1]) for i in user_inc), 2)
            sum_exp = round(sum(float(i[1]) for i in user_exp), 2)
            date = self.date_pattern(date=user_inc[0][2] if user_inc else user_exp[0][2],
                                     within=within)
            pattern = f"<u>Доходы {date}</u>:\n{inc_rep}---\n<b>Итого:</b> {sum_inc} {cur}\n\n" \
                      f"<u>Расходы {date}</u>:\n{exp_rep}---\n<b>Итого:</b> {sum_exp} {cur}"
        return pattern
