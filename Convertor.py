from decimal import Decimal

from forex_python.converter import CurrencyRates


class Convertor:

    def __init__(self):
        self.c = CurrencyRates()

    def get_rates(self, convert_to):
        convert_rate = self.c.get_rates(convert_to)
        return convert_rate

    def convert(self, convert_from, convert_to, convert_amount):
        converted_amount = self.c.convert(convert_from, convert_to, Decimal(convert_amount))
        return converted_amount
