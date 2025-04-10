# utils.py

from aiogram import types
from aiogram.filters import BaseFilter

class TextEquals(BaseFilter):
    def __init__(self, equals: str, ignore_case: bool = True):
        self.equals = equals.lower() if ignore_case else equals
        self.ignore_case = ignore_case

    async def __call__(self, message: types.Message) -> bool:
        text = message.text or ""
        if self.ignore_case:
            return text.lower() == self.equals
        return text == self.equals

def format_currency(value):
    """
    Форматирует число как валюту с разделением тысяч и двумя знаками после запятой.
    """
    try:
        formatted = f"{value:,.2f}".replace(",", " ")
        return formatted
    except Exception as e:
        return str(value)
