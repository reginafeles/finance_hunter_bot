"""
Test xlsx_manager module
"""
import unittest

from datetime import datetime
import openpyxl

from database_handling.xlsx_manager import ExcelManager
from auxiliary_files.constants import PROJECT_ROOT


class ExcelManagerTest(unittest.TestCase):
    """
    Checks excel_manager module
    """
    def setUp(self) -> None:
        """
        Creates an object of ExcelManager class and an excel table
        """
        self.exm = ExcelManager()
        self.workbook = openpyxl.load_workbook(PROJECT_ROOT / "FinanceHunterBot.xlsx")

    def test_change_cur_name(self):
        """
        Checks whether there are two sheets in the table having needed names
        """
        sheet_names = self.workbook.sheetnames
        self.assertEqual(sheet_names, ['Доходы', 'Расходы'])
        self.assertEqual(len(sheet_names), 2)

    def get_sheets_data(self, sheet_name, column_names):
        """
        Extracts data from the table
        """
        sheet_range = self.workbook[sheet_name]
        columns_data = []
        for name in column_names:
            column = sheet_range[name]
            values = []
            for val in column:
                values.append(val.value)
            columns_data.append(values)
        return columns_data

    def test_column_values(self):
        """
        Checks whether data has needed format
        """
        sheet_names = ['Доходы', 'Расходы']
        for name in sheet_names:
            sheets_data = self.get_sheets_data(name, ['A', 'B', 'C'])
            for i in sheets_data[0][1:]:
                self.assertTrue(isinstance(i, str) or i is None)
            for i in sheets_data[1][1:]:
                self.assertTrue(isinstance(i, (float, int)) or i is None)
            for i in sheets_data[2][1:]:
                self.assertTrue((isinstance(i, str) and datetime.strptime(i, '%d-%m-%Y')
                                 or i is None))
