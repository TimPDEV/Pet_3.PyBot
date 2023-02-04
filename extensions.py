import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена, введите другую")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена, введите другую")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={quote_key}")
        resp = json.loads(r.content)
        new_price = resp['rates'][quote_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message
