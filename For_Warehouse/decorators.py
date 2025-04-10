# decorators.py
import logging
import functools

def log_exceptions(func):
    """
    Декоратор для логирования вызова функции и любых возникающих исключений.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Функция {func.__name__} успешно выполнена.")
            return result
        except Exception as err:
            logging.error(f"Ошибка в функции {func.__name__}: {err}", exc_info=True)
            raise
    return wrapper
