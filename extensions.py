import requests
import json
from config import API, keys


class ExchangerException(Exception):
    pass


class Exchanger:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ExchangerException(f'Невозможно перевести одинаковые валюты "{quote}"')
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise ExchangerException(f'Неправильно введена валюта "{quote}"')
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise ExchangerException(f'Неправильно введена валюта "{base}"')
        try:
            amount = float(amount)
        except ValueError:
            raise ExchangerException(f'Неправильно введено количество валюты "{amount}"')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API}/latest/{quote_key}')
        total_value = json.loads(r.content)['conversion_rates'][base_key]
        return amount * total_value
