# reports.py

import pandas as pd
from datetime import datetime, timedelta
import logging
from excel_manager import ExcelManager
from decorators import log_exceptions
import config

# Глобальный экземпляр ExcelManager
excel_manager = ExcelManager(config.settings.EXCEL_FILE)

@log_exceptions
def generate_report(sheet_move: str, sheet_price: str, date_column: str,
                    quantity_column: str, days: int, report_title: str) -> str:
    """
    Генерирует отчёт за последние `days` дней для указанной операции.
    """
    # Читаем данные о движении и прайс-лист
    df_move = excel_manager.read_sheet_as_df(sheet_move)
    df_price = excel_manager.read_sheet_as_df(sheet_price)
    
    # Приводим колонку с датой к формату datetime
    df_move[date_column] = pd.to_datetime(df_move[date_column], dayfirst=True, errors='coerce')
    
    current_date = datetime.today()
    delta = timedelta(days=days)
    
    # Фильтруем данные по дате: разница между текущей датой и датой операции должна быть меньше delta
    df_filtered = df_move[current_date - df_move[date_column] <= delta]
    if df_filtered.empty:
        return f"🚫 <i>Нет данных за последние {days} дней</i>"
    
    # Объединяем данные с прайс-листом по полю "Наименование товара"
    df_merged = pd.merge(df_filtered, df_price, how='left', on='Наименование товара')
    df_merged['Стоимость'] = df_merged['Стоимость'].fillna(0)
    df_merged['Сумма'] = df_merged['Стоимость'] * df_merged[quantity_column]
    
    # Группируем по товару и суммируем
    df_report = df_merged[['Наименование товара', quantity_column, 'Сумма']].groupby('Наименование товара', as_index=False).sum()
    df_report[quantity_column] = df_report[quantity_column].fillna(0)
    df_report['Сумма'] = df_report['Сумма'].fillna(0)
    
    # Формируем строки отчёта
    report_lines = [
        f"🔹 <b>{row['Наименование товара']}</b> — <code>{int(row[quantity_column])} шт.</code> (<i>{int(row['Сумма'])} руб.</i>)"
        for _, row in df_report.iterrows() if int(row[quantity_column]) > 0
    ]
    return f"📦 <b>{report_title} за {days} дней:</b>\n\n" + "\n".join(report_lines)

def generate_stock_report(days: int, operation: str) -> str:
    """
    Универсальная функция для генерации отчёта по складу для операции "delivery" (поступления) или
    "shipment" (отгрузки) за последние `days` дней.

    :param days: Количество дней для выборки.
    :param operation: Тип операции: "delivery" для поступлений, "shipment" для отгрузок.
    :return: Строка с сформированным отчётом.
    """
    if operation == "delivery":
        quantity_column = "Поступление"
        report_title = "Поступления"
    elif operation == "shipment":
        quantity_column = "Отгрузка"
        report_title = "Отгрузки"
    else:
        return f"❌ Ошибка: неизвестный тип операции '{operation}'."
    
    return generate_report(
        sheet_move=config.settings.SHEET_MOVE,
        sheet_price=config.settings.SHEET_PRICE,
        date_column="Дата",
        quantity_column=quantity_column,
        days=days,
        report_title=report_title
    )
