"""
There are the names of categories and links to them
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Markup:
    """
    Creates the buttons
    """
    def __init__(self):
        pass

    @staticmethod
    def start_markup():
        """
        Creates initial buttons
        """
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton('📈 Доходы', callback_data='cb_income'),
            InlineKeyboardButton('📉 Расходы', callback_data='cb_expense'),
            InlineKeyboardButton('💱 Валюта учёта', callback_data='cb_currency'),
            InlineKeyboardButton('📊 Отчёт', callback_data='cb_report')
        )
        return markup

    @staticmethod
    def income_markup():
        """
        Creates options in 📈 Доходы
        """
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton('📈 Зарплата', callback_data='📈 Зарплата'),
            InlineKeyboardButton('📈 Пособие', callback_data='📈 Пособие'),
            InlineKeyboardButton('📈 Пенсия', callback_data='📈 Пенсия'),
            InlineKeyboardButton('📈 Сдача квартиры в аренду',
                                 callback_data='📈 Сдача квартиры в аренду'),
            InlineKeyboardButton('📈 Стипендия', callback_data='📈 Стипендия'),
            InlineKeyboardButton('➕ Другое', callback_data='➕ Другое'),
            InlineKeyboardButton('🔙 Назад', callback_data='back')
        )
        return markup

    @staticmethod
    def expense_markup():
        """
        Creates optopns in 📉 Расходы
        """
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton('🛒 Продукты', callback_data='🛒 Продукты'),
            InlineKeyboardButton('💊 Здоровье', callback_data='💊 Здоровье'),
            InlineKeyboardButton('🚌 Транспорт', callback_data='🚌 Транспорт'),
            InlineKeyboardButton('👕 Одежда, товары', callback_data='👕 Одежда, товары'),
            InlineKeyboardButton('📄 Коммунальные платежи', callback_data='📄 Коммунальные платежи'),
            InlineKeyboardButton('🚘 Автомобиль', callback_data='🚘 Автомобиль'),
            InlineKeyboardButton('📞 Интернет и связь', callback_data='📞 Интернет и связь'),
            InlineKeyboardButton('📚 Образование', callback_data='📚 Образование'),
            InlineKeyboardButton('🏡 Дом, ремонт', callback_data='🏡 Дом, ремонт'),
            InlineKeyboardButton('🏠 Аренда жилья', callback_data='🏠 Аренда жилья'),
            InlineKeyboardButton('🌈 Развлечения', callback_data='🌈 Развлечения'),
            InlineKeyboardButton('➖ Другое', callback_data='➖ Другое'),
            InlineKeyboardButton('🔙 Назад', callback_data='back')
        )
        return markup

    @staticmethod
    def currency_markup():
        """
        Creates options in 💱 Валюта учёта
        """
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton('Рубль ₽', callback_data='₽'),
            InlineKeyboardButton('Доллар $', callback_data='$'),
            InlineKeyboardButton('Евро €', callback_data='€'),
            InlineKeyboardButton('🔙 Назад', callback_data='back')
        )
        return markup

    @staticmethod
    def report_period_markup():
        """
        Add the buttons for finance report
        """
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton('🗓 День', callback_data='day'),
            InlineKeyboardButton('🗓 Неделя', callback_data='week'),
            InlineKeyboardButton('🗓 Месяц', callback_data='month'),
            InlineKeyboardButton('🗓 Год', callback_data='year'),
            InlineKeyboardButton('🗓 Все записи', callback_data='all_records')
        )
        return markup

    @staticmethod
    def report_place_markup():
        """
        Add the buttons for finance report
        """
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton('↙ Импортировать сюда', callback_data='here'),
            InlineKeyboardButton('↗ Экспортировать в xlsx', callback_data='there')
        )
        return markup
