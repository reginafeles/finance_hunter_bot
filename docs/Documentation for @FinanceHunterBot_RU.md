# Техническая документация для [@FinanceHunterBot](https://t.me/FinanceHunterBot)

- *[README.md](https://github.com/eskondrashova/FinanceHunterBot/blob/8d0932de66fd1a1b4205245e977dea22bfcf4a03/README.md)*
- *[Руководство пользователя на английском языке](https://github.com/eskondrashova/FinanceHunterBot/blob/main/docs/User's%20Manual_ENG.md)*
- *[Техническая документация на английском языке](https://github.com/eskondrashova/FinanceHunterBot/blob/main/docs/Documentation%20for%20%40FinanceHunterBot_ENG.md)*

## Основные файлы

### [**`currency_converter.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/bot_functions/currency_converter.py)

Конвертер валют для кнопки `Выбор валюты`. Он использует библиотеки [requests](https://pypi.org/project/requests/) и [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) внутри класса `CurrencyConverter` для запроса и парсинга курсов валют с сайта https://www.x-rates.com/.

|метод|операция|
|---|---|
|`change_cur_name`|преобразует символ в название|
|`get_exchange_coefs`| парсит ответ с сайта https://www.x-rates.com/ и получает курсы валют|
|`get_coef`|использует курсы обмена для нужной пары|

### [**`db.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/database/db.py)

`db.py` работает с базой данных пользователей. С помощью библиотеки [sqlite3](https://docs.python.org/3/library/sqlite3.html) формируется и инициируется класс `BotDB`, который создаёт и управляет таблицей типа .db. Экземпляр BotDB может создавать таблицу пользователей и таблицу их записей. Он может модифицировать вышеупомянутые таблицы.

> Для прямого доступа к таблице .db в файле [`accountant.db`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/accountant.db) необходимо установить программу [SQLite](https://www.sqlite.org/).

|метод|операция|
|---|---|
|`create_users_table`|создать .db таблицу для хранения информации о пользователях|
|`create_records_table`|создать .db таблицу для записи информации об операциях|
|`user_exists`|проверяет, не создан ли уже пользователь в таблице .db.|
|`add_user`|добавить пользователя в таблицу записей|
|`get_currency`|извлечь валюту по user_id|
|`get_id`|извлечь id пользователя|
|`add_record`|добавить доход или расход пользователя в таблицу операций|
|`change_cur_name`|изменение названия валюты в таблице операций|
|`get_inc_exp`|извлечение доходов или расходов из таблицы операций на основе требуемых временных рамок|
|`delete_history`|удаляет информацию о пользователе в таблице операций|
|`close`|закрывает таблицу|

### [**`markups.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/bot_functions/markups.py)

Файл `markups.py` управляет маркапами бота. Он использует библиотеку [aiogram](https://docs.aiogram.dev/) для построения структуры маркапов или, иначе говоря, кнопками бота, в частности с помощью `InlineKeyboardMarkup` и `InlineKeyboardButton`. 

> Категории для доходов и расходов импортируются из [`categories.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/categories.py). 

Функции файла:

- `start_markup` создает начальные кнопки;
- `income_markup` добавляет опции в `📈 Доходы`;
- `expense_markup` добавляет опции в `📉 Расходы`;
- `currency_markup` добавляет опции в `💱 Валюта учёта`;
- `report_period_markup` и `report_place_markup` добавляют кнопки для финансового отчета.

### [**`server.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/server.py)

**Этот файл содержит структуру главного бота.**.

[aiogram](https://docs.aiogram.dev/) является основным источником архитектуры бота. Она реализуется внутри структуры класса `Server`.

Импорты:

- Discpatcher отвечает за создание обработчиков для сообщений пользователя. Например, @dp.message_handler(commands=['start']) означает, что пользователь печатает `/start`, что приводит к действиям, заложенным в этом обработчике. Обработчик @dp.callback_query_handler работает аналогичным образом, но обрабатывает диапазон возможных ответов. 
- С каждым обработчиком реализуется определенная функция asynch.

Кроме того, импортируются следующие константы и структуры:

- `TOKEN` из `config.py`
- класс `CurrencyConverter` из [`currency_converter.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/currency_converter.py)
- класс `Markup` из [`markups.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/markups.py)
- класс `UsersManager` из [`users_manager.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/users_manager.py)
- класс `ExcelManager` из [`xlsx_manager.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/xlsx_manager.py)

> Расширенная информация об импортируемых классах приведена в соответствующих частях этой документации.

| асинхронная функция | Реализованная логика | Специальные утилиты |
|---|---|---|
| `send_welcome` | отвечает на команду `/start`, отправленную пользователем | @dp.message_handler, `cur_user` экземпляр `UsersManager` | `send_welcome`.
| `send_help` | отвечает на команду `/help`, отправленную пользователем | @dp.message_handler |
| `delete_history` | удаляет историю событий пользователя | @dp.message_handler, `cur_user` экземпляр `UsersManager` |
| `handle_start_cbq` | обрабатывает нажатие начальных 4 кнопок в боте | @dp.callback_query_handler с лямбдой, `cur_user` экземпляр `UsersManager` |
| `send_menu` | возвращает пользователя в главное меню | @dp.callback_query_handler |
| `handle_income_cbq` | обрабатывает входные данные | @dp.callback_query_handler с лямбдой, класс Category |
| `get_sum` | проверяет достоверность введенной суммы денег | @dp.message_handler, `cur_user` экземпляр `UsersManager` | }
| `change_currency` | обрабатывает выбор валюты | @dp.callback_query_handler c лямбдой, `cur_user` экземпляр `UsersManager` |
| `process_report_period` | управляет экспортом финансов в нужной форме | @dp.callback_query_handler с лямбдой, `excel` экземпляр класса `ExcelManager` | |
| `send_statistics` | дополнение к `process_report_period`, отвечающее за период нужного отчета, `cur_user` экземпляр класса `UsersManager` | @dp.callback_query_handler с лямбдой | @dp.callback_query_handler.

`__main__` запускает бота и включает игнорирование всех отправленных сообщений, пока бот был неактивен.

### [**`users_manager.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/users_manager.py)

Этот файл создает класс, отвечающий за обработку информации о пользователях, `UsersManager`.

Импорты:

- `datetime`, `locale` обрабатывают дату и время и устанавливают последнее в UTC+3. 

Используется перед классом с `setlocale` и в методе `date_pattern`, который извлекает нужные временные рамки из текущей даты.

- `BotDB` из [`db.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/db.py). Экземпляр этого класса `db` управляет записями пользователей (добавление, удаление информации о доходах, расходах, выбор текущей валюты):

| метод | назначение |
 |---|---|---|
 | `register_user` | добавление пользователя в базу данных |
 | `get_user_currency` | извлечение из базы данных выбранной пользователем валюты |
 | `add_user_record` | добавление операции пользователя |
 | `change_user_currency` | изменить валюту, выбранную пользователем в базе данных |
 | `text_pattern` | создаёт формат строки str из строки базы данных |
 | `date_pattern` | извлекает время из текущей даты |

### [**`xlsx_manager.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/xlsx_manager.py)

Этот файл отвечает за экспорт в формат .xlsx.

Импорт:

- `openpyxl`, который поддерживает работу с файлами .xlsx
- `datetime` для записи даты и времени для каждой операции в базе данных
- Класс `BotDB` из [db.py](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database/db.py)

> Информация для таблицы Excel берется из базы данных .db

Методы ExcelManager:

|имя|предназначение|
|---|---|
|`set_format`|форматирование даты|
|`get_records`|извлекает доходы и расходы из экземпляра базы данных|
|`fill_excel`| заполняет лист Excel извлеченной информацией.
|`save_excel`|создает и сохраняет лист Excel под именем `Acountant_Bot.xlsx`|.

## Другие файлы

| Файл | Реализованная логика | Особенности |
|---|---|---|
| [`accountant.db`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/accountant.db) | Таблица SQLite для управления информацией о пользователе | [SQLite](https://www.sqlite.org/) программное обеспечение |
| `config.py` | содержит токен бота | TOKEN константа |
| [`constants.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/auxiliary_files/constants.py) | устанавливает корневую папку проекта | [pathlib](https://docs.python.org/3/library/pathlib.html) библиотека|
| [`start.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/start.py) | запускает бота | | |
| [`requirements.txt`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/requirements.txt) | указывает необходимые пакеты и их версии для нормальной работы бота | **обязательно установить все пакеты из этого файла перед запуском бота** | |
