"""
Parses currency exchange rates from https://www.x-rates.com/ site
"""
import requests
from bs4 import BeautifulSoup as bs


class CurrencyConverter:
    """
    Changes the currency
    """
    def __init__(self, old_cur):
        self.old_cur = old_cur

    def change_cur_name(self):
        """
        Converts a symbol to a name
        """
        curs = {'₽': 'RUB',
                '$': 'USD',
                '€': 'EUR'}
        return curs[self.old_cur]

    def get_exchange_coefs(self):
        """
        Parses the response from https://www.x-rates.com/ and gets the exchange rates
        """
        res = requests.get(f"https://www.x-rates.com/table/?from={self.change_cur_name()}&amount=1",
                            timeout=1)
        soup = bs(res.text, "html.parser")

        exchange_tables = soup.find_all("table")
        exchange_coefs = {}
        for ex_tab in exchange_tables:
            for selector in ex_tab.find_all("tr"):
                tds = selector.find_all("td")
                if tds:
                    cur_name = tds[0].text
                    coef = float(tds[1].text)
                    exchange_coefs[cur_name] = coef
        return exchange_coefs

    def get_coef(self, new_cur):
        """
        Uses the exchange rates for the required pair
        """
        coefs = self.get_exchange_coefs()
        coef = None
        if new_cur == '₽':
            coef = coefs['Russian Ruble']
        elif new_cur == '$':
            coef = coefs['US Dollar']
        elif new_cur == '€':
            coef = coefs['Euro']
        return coef
