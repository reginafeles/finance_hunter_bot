"""
This file contains the main bot's structure
"""
from aiogram import Bot, Dispatcher, types, executor
from auxiliary_files.config import TOKEN

from bot_functions.markups import Markup

from bot_functions.currency_converter import CurrencyConverter
from database_handling.users_manager import UsersManager
from database_handling.xlsx_manager import ExcelManager

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
cur_user = UsersManager()
markup = Markup()

call_data_history = []


class Server:
    """
    Contains FinanceHunterBot's logic
    """

    def __init__(self):
        self.answer = None
        self.from_user = None
        self.data = None
        self.message = None
        self.text = None

    @dp.message_handler(commands=['start'])
    async def send_welcome(self: types.Message):
        """
        Answers /start command sent by user
        """
        text = f"Здравствуйте, {self.from_user.first_name}!\n" \
               f"Вас приветствует <b><i>Бот для учёта финансов</i></b>!"
        await bot.send_message(
            self.from_user.id,
            text=text,
            parse_mode='html', reply_markup=markup.start_markup())
        cur_user.register_user(self.from_user.id)

    @dp.message_handler(commands=['help'])
    async def send_help(self: types.Message):
        """
        Answers /help command sent by user
        """
        await bot.send_message(
            self.from_user.id,
            text=
            "<b><i>Помощь по боту</i></b>\n\n"
            "Вы находитесь в <u>главном меню</u>.\n"
            "- Нажмите <i>📈 Доходы</i>, чтобы добавить запись о доходах;\n"
            "- Нажмите <i>📉 Расходы</i>, чтобы добавить запись о расходах;\n"
            "- Нажмите <i>💱 Валюта учёта</i>, чтобы изменить текущую валюту;\n"
            "- Нажмите <i>📊 Отчёт</i>, чтобы посмотреть записи о доходах / расходах",
            parse_mode='html', reply_markup=markup.start_markup())

    @dp.message_handler(commands=['delete'])
    async def delete_history(self: types.Message):
        """
        Deletes the finances' history of the user
        """
        cur_user.d_b.delete_history(user_id=self.from_user.id)
        await bot.send_message(
            self.from_user.id,
            text="Записи удалены!")

    @dp.callback_query_handler(lambda call:
                               call.data in ['cb_income', 'cb_expense', 'cb_currency', 'cb_report'])
    async def handle_start_cbq(self: types.CallbackQuery):
        """
        Handles the press of the initial 4 buttons of the bot
        """
        if self.data == 'cb_income':
            await self.message.answer(
                text='📈 Выберите категорию:', reply_markup=markup.income_markup())
        elif self.data == 'cb_expense':
            await self.message.answer(
                text='📉 Выберите категорию:', reply_markup=markup.expense_markup())
        elif self.data == 'cb_currency':
            await self.message.answer(text=f'💱 Выберите валюту\nВалюта сейчас: '
                                           f'{cur_user.get_user_cur(self.from_user.id)}',
                                      reply_markup=markup.currency_markup())
        elif self.data == 'cb_report':
            await self.message.answer(
                text='Посмотреть отчёт:', reply_markup=markup.report_place_markup())

    @dp.callback_query_handler(text='back')
    async def send_menu(self: types.CallbackQuery):
        """
        Brings the user back to the main menu
        """
        await self.message.answer('🔎 Выберите нужный раздел:', reply_markup=markup.start_markup())

    @dp.callback_query_handler(lambda callback_query:
                               callback_query.data in ['📈 Зарплата',
                                                       '📈 Пособие',
                                                       '📈 Пенсия',
                                                       '📈 Сдача квартиры в аренду',
                                                       '📈 Стипендия',
                                                       '➕ Другое'])
    async def handle_income_cbq(self: types.CallbackQuery):
        """
        Handles income input
        """
        await self.message.answer(text='💰 Введите сумму:')
        call_data_history.extend([self.data, 1])
        await self.message.delete()

    @dp.callback_query_handler(lambda callback_query:
                               callback_query.data in ['🛒 Продукты',
                                                       '💊 Здоровье',
                                                       '🚌 Транспорт',
                                                       '👕 Одежда, товары',
                                                       '📄 Коммунальные платежи',
                                                       '🚘 Автомобиль',
                                                       '📞 Интернет и связь',
                                                       '📚 Образование',
                                                       '🏡 Дом, ремонт',
                                                       '🏠 Аренда жилья',
                                                       '🌈 Развлечения',
                                                       '➖ Другое'])
    async def handle_expense_cbq(self: types.CallbackQuery):
        """
        Handles expense input
        """
        await self.message.answer(text='💰 Введите сумму:')
        call_data_history.extend([self.data, -1])
        await self.message.delete()

    @dp.message_handler(content_types=['text'])
    async def get_sum(self: types.Message):
        """
        Checks the validity of the money input
        """
        if call_data_history:
            if self.text.isdigit():
                cur_user.add_user_record(user_id=self.from_user.id, category=call_data_history[0],
                                         operation=call_data_history[1], value=self.text)
                await bot.send_message(
                    self.from_user.id,
                    text='✅ Записано!', reply_markup=markup.start_markup())
                call_data_history.clear()
            else:
                await bot.send_message(
                    self.from_user.id,
                    text='❌ Неверный формат ввода! Попробуйте ещё раз.')

    @dp.callback_query_handler(lambda call: call.data in ['₽', '$', '€'])
    async def change_currency(self: types.CallbackQuery):
        """
        Handles the currency choices
        """
        cur_con = CurrencyConverter(cur_user.get_user_cur(self.from_user.id))
        if self.data == cur_user.get_user_cur(self.from_user.id):
            await self.message.answer(text="Эта валюта используется сейчас!\n"
                                      "Выберите другую валюту или нажмите <i>🔙 Назад</i>",
                                      parse_mode='html')
        else:
            cur_user.change_user_currency(user_id=self.from_user.id,
                                          new_cur=self.data,
                                          coef=cur_con.get_coef(self.data))
            await self.message.answer(text="✔ Валюта успешно выбрана!",
                                      reply_markup=markup.start_markup())
            await self.message.delete()

    @dp.callback_query_handler(lambda call: call.data in ['here', 'there'])
    async def process_report_period(self: types.CallbackQuery):
        """
        Manages the finances' export in the required form
        """
        if self.data == 'here':
            await self.message.answer(
                text='📆 Выберите отчётный период:', reply_markup=markup.report_period_markup()
            )
        elif self.data == 'there':
            excel = ExcelManager()
            excel.save_excel(user_id=self.from_user.id)
            await self.message.answer_document(types.InputFile('FinanceHunterBot.xlsx'),
                                               reply_markup=markup.start_markup())

    @dp.callback_query_handler(lambda call:
                               call.data in ['day', 'week', 'month', 'year', 'all_records'])
    async def send_statistics(self: types.CallbackQuery):
        """
        Addition to process_report_period,
        responsible for the period of the desired report,
        cur_user instance of UsersManager
        """
        if self.data == 'day':
            await self.message.answer(
                text=(cur_user.show_statistics(self.from_user.id, within='day')),
                parse_mode='html',
                reply_markup=markup.start_markup()
            )
        elif self.data == 'week':
            await self.message.answer(
                text=(cur_user.show_statistics(self.from_user.id, within='week')),
                parse_mode='html',
                reply_markup=markup.start_markup()
            )
        elif self.data == 'month':
            await self.message.answer(
                text=(cur_user.show_statistics(self.from_user.id, within='month')),
                parse_mode='html',
                reply_markup=markup.start_markup()
            )
        elif self.data == 'year':
            await self.message.answer(
                text=(cur_user.show_statistics(self.from_user.id, within='year')),
                parse_mode='html',
                reply_markup=markup.start_markup()
            )
        elif self.data == 'all_records':
            await self.message.answer(
                text=(cur_user.show_statistics(self.from_user.id, within='all')),
                parse_mode='html',
                reply_markup=markup.start_markup()
            )


def start():
    """
    Polls Server
    """
    executor.start_polling(dp, skip_updates=True)
