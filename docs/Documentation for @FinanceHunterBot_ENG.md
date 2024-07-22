# Techincal Documentation for [@FinanceHunterBot](https://t.me/FinanceHunterBot)

- *[User's Manual in English](https://github.com/eskondrashova/FinanceHunterBot/blob/main/docs/User's%20Manual_ENG.md)*
- *[README.md (Russian)](https://github.com/eskondrashova/FinanceHunterBot/blob/main/README.md)*
- *[Technical Documentation in Russian](https://github.com/eskondrashova/FinanceHunterBot/blob/main/docs/Documentation%20for%20%40FinanceHunterBot_RU.md)*

## Main files

### [**`currency_converter.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/bot_functions/currency_converter.py)

Currency converter for `Выбор валюты` button. It uses [requests](https://pypi.org/project/requests/) and [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) libraries within `CurrencyConverter` class for requesting and parsing currency exchange rates from https://www.x-rates.com/ site.

|methods|operation|
|---|---|
|`change_cur_name`|converts a symbol to a name|
|`get_exchange_coefs`|parses the response from  https://www.x-rates.com/ and gets the exchange rates|
|`get_coef`|uses the exchange rates for the required pair|

### [**`db.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/database/db.py)

`db.py` deals with users' database. With [sqlite3](https://docs.python.org/3/library/sqlite3.html) library it builds and initiates a `BotDB` class, which creates and manages a .db type table. A BotDB instance can create users' table and their records' table. It can modify the aforementioned tables.

> To access a .db table directly in [`accountant.db`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/accountant.db) file, one needs [SQLite](https://www.sqlite.org/) software installed.

|method|operation|
|---|---|
|`create_users_table`|create a .db table for users information|
|`create_records_table`|create a .db table for records information|
|`user_exists`|checks whether the user is already created in a .db table|
|`add_user`|add user to records' table|
|`get_currency`|exctract currency from by user_id|
|`get_id`|exctract user id|
|`add_record`|add expense or income to a user in a records' sheet|
|`change_cur_name`|currency name change in records|
|`get_inc_exp`|extract income or expenditure from records based on required timeframe|
|`delete_history`|deletes information from the user in records table|
|`close`|closes the table|

### [**`markups.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/main/bot_functions/markups.py)

`markups.py` file manages bot's markups. It uses [aiogram](https://docs.aiogram.dev/) library in order to build markups structure, `InlineKeyboardMarkup` and `InlineKeyboardButton` specifically. 

> Categories for each income and expenditure are imported from [`categories.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/categories.py) 

File's functions:

- `start_markup` creates initial buttons;
- `income_markup` creates options in `📈 Доходы`;
- `expense_markup` creates optopns in `📉 Расходы`;
- `currency_markup` creates options in `💱 Валюта учёта`;
- `report_period_markup` and `report_place_markup` add the buttons for finance report.

### [**`server.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/server.py)

**This file contains the main bot's structure.**

[aiogram](https://docs.aiogram.dev/) is implemented as the main source for the bot's architechture. It's realized within the structure of the class `Server`.

Imports:

- Discpatcher is responsible for creation of handlers for the user's messages. E.g. @dp.message_handler(commands=['start']) means that the user is printing `/start` which leads to actions incased in this handler. @dp.callback_query_handler works in the same manner but deals with a range of possible answers. 
- A specified asynch function is implemented with each handler.

Additionally, the following constants and structures are imported:

- `TOKEN` from `config.py`
- class `CurrencyConverter` from [`currency_converter.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/currency_converter.py)
- class `Markup` from [`markups.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/bot_functions/markups.py)
- class `UsersManager` from [`users_manager.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/users_manager.py)
- class `ExcelManager` from [`xlsx_manager.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/xlsx_manager.py)

> Extended infromation for the imported classes is listed in the relevant parts of this doccumentation.

| asynch function | Realised logic | Special utilities |
|---|---|---|
| `send_welcome` | answers `/start` command sent by user | @dp.message_handler, `cur_user` instance of `UsersManager` |
| `send_help` | answers `/help` command sent by user | @dp.message_handler |
| `delete_history` | deletes the finances' history of the user | @dp.message_handler, `cur_user` instance of `UsersManager` |
| `handle_start_cbq` | handles the press of the initial 4 buttons oin the bot | @dp.callback_query_handler with lambda, `cur_user` instance of `UsersManager` |
| `send_menu` | brings the user back to the main menu | @dp.callback_query_handler |
| `handle_income_cbq` | handles income input | @dp.callback_query_handler with lambda, Category class |
| `get_sum` | checks the validity of the money input | @dp.message_handler, `cur_user` instance of `UsersManager` |
| `change_currency` | handles the currency choice | @dp.callback_query_handler with lambda, `cur_user` instance of `UsersManager` |
| `process_report_period` | manages the finances' export in the required form | @dp.callback_query_handler with lambda, `excel` instance of `ExcelManager` class |
| `send_statistics` | addition to `process_report_period`, responsible for the period of the desired report, `cur_user` instance of `UsersManager` | @dp.callback_query_handler with lambda |

`__main__` starts the bot and enables ignoration of any messages sent while the bot was inactive.

### [**`users_manager.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/users_manager.py)

This file creates the class responsible for handling users' information, `UsersManager`.

Imports:

- `datetime`, `locale` handle date and time and sets the latter to UTC+3. 

It is used before the class with `setlocale` and in the `date_pattern` method, which extracts the required timframe from the current date.

- `BotDB` from [`db.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/main/db.py). The instance of this class, `db` manages the records of the users (addition, deletion of infomation about the income, expenditure, current currency choice):

 | method | purpose |
 |---|---|---|
 | `register_user` | add a user to database |
 | `get_user_currency` | extract the user's currency choice from the database |
 | `add_user_record` | add an operation of the user |
 | `change_user_currency` | change the user's currecny choice in the database |
 | `text_pattern` | creates a string from the database |
 | `date_pattern` | extracts the required timeframe from the current date |

### [**`xlsx_manager.py`**](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database_handling/xlsx_manager.py)

This file is responsible for export in .xlsx format.

Imports:

- `openpyxl`, which supports handling of .lxsx files
- `datetime` for date and time record for each operation in the database
- `BotDB` class from [db.py](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/database/db.py)

> The information for the Excel sheet is taken from .db database

ExcelManager methods:

|name|purpose|
|---|---|
|`set_format`|date formatting|
|`get_records`|extracts income and expenses from db instance|
|`fill_excel`|fills the Excel sheet with exsiting exctracted information|
|`save_excel`|creates and saves the Excel sheet under the name `Acountant_Bot.xlsx`|

## Other files

| File | Realised logic | Specialties |
|---|---|---|
| [`accountant.db`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/accountant.db) | SQLite table for managing user's information | [SQLite](https://www.sqlite.org/) software |
| `config.py` | contains bot's token | TOKEN constant |
| [`constants.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/auxiliary_files/constants.py) | sets project's root folder | [pathlib](https://docs.python.org/3/library/pathlib.html) library|
| [`start.py`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/start.py) | starts the bot | |
| [`requirements.txt`](https://github.com/eskondrashova/FinanceHunterBot/blob/1597fbaba602a73f4427baf181cb248ca2a19d8c/requirements.txt) | states the required packeges and their versions for the current bot to function properly | **it is obligatory to install all packages from this file before starting the bot** |
