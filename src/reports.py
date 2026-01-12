import logging
import os
from datetime import datetime

import pandas as pd

from config import ROOT_DIR

current_dir = os.path.dirname(__file__)
absolute_path = os.path.join(current_dir, "..")
os.chdir(absolute_path)
logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler_reports = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8")
file_formatter_reports = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler_reports.setFormatter(file_formatter_reports)
logger.addHandler(file_handler_reports)


def report_output(filename="report_output.xlsx"):
    """Декоратор для вывода отчета"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, str):
                return result
            else:
                result.to_excel(f"{ROOT_DIR}/data/{filename}", index=False)
                result = result.to_json(date_format="iso", force_ascii=False)
                # result = json.dumps(result, ensure_ascii=False)
                print(result)
                return result

        return wrapper

    return decorator


@report_output()
def expenses_by_category(transactions, category, optional_date=None):
    """Функция показывающая траты за последние 3 месяца"""

    if optional_date is None:
        optional_date_1 = datetime.today()
        optional_date = optional_date_1.strftime("%Y-%m-%d")
        year = int(optional_date_1.strftime("%Y"))
        month = int(optional_date_1.strftime("%m"))
        day = int(optional_date_1.strftime("%d"))
    else:
        optional_date = datetime.strptime(optional_date, "%Y-%m-%d")
        year = optional_date.year
        month = optional_date.month
        day = optional_date.day
    logger.debug("Определена дата опциональная дата")

    for i in range(3):
        month = month - 1
        if month == 0:
            month = 12
            year -= 1
    start_date = datetime(year, month, day)
    logger.debug("Определена дата начала диапазона дат")

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    transactions_expenses_df = transactions[transactions["Сумма операции"] < 0]
    transactions_in_the_date_range = transactions_expenses_df.loc[
        start_date <= transactions_expenses_df["Дата платежа"]
    ].loc[transactions_expenses_df["Дата платежа"] <= optional_date]
    logger.debug("Список операций отсортирован по диапазону дат")

    sort_transactions_expenses_df = transactions_in_the_date_range[
        transactions_in_the_date_range["Категория"] == category
    ]
    logger.debug("Определены операции выбранной категории")
    if len(sort_transactions_expenses_df) == 0:
        sort_transactions_expenses_df = "Операций не найдено"

    return sort_transactions_expenses_df
