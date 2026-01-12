import json
import logging
import os
from datetime import datetime

import pandas as pd

from src.utils import (
    currency,
    reading_operations_xlsx,
    separation_of_expenses,
    separation_of_receipts,
    sorted_category_expenses,
    sorted_receipts,
    stock_prices,
)

current_dir = os.path.dirname(__file__)
absolute_path = os.path.join(current_dir, "..")
os.chdir(absolute_path)
logger = logging.getLogger("views")
logger.setLevel(logging.DEBUG)
file_handler_views = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8")
file_formatter_views = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler_views.setFormatter(file_formatter_views)
logger.addHandler(file_handler_views)


def sorting_events(selected_date, start_date=None):
    """Функция сортирующая операции в указанном диапазоне дат"""

    selected_date = datetime.strptime(selected_date, "%Y-%m-%d")
    if start_date is None:
        start_date = datetime(selected_date.year, selected_date.month, 1)
    logger.debug("Определена начальная дата диапазона")

    dir_data = os.getcwd()
    absolute_path = os.path.join(dir_data, "..")
    os.chdir(absolute_path)
    path_to_direct = os.path.dirname(__file__)
    path_to_file_json = os.path.join(path_to_direct, "..", "data", "user_settings.json")

    with open(path_to_file_json, "r", encoding="utf-8") as read_file:
        user_settings = json.load(read_file)
        symbols = ", ".join(user_settings["user_currencies"])
        list_stock = user_settings["user_stocks"]
        logger.debug("Из файла json взяты получены валюты и акции для последующей обработки")

    transactions = reading_operations_xlsx()
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)

    transactions_in_the_date_range = transactions.loc[start_date <= transactions["Дата платежа"]].loc[
        transactions["Дата платежа"] <= selected_date
    ]
    logger.debug("Определены операции в диапазоне дат")

    list_key = list(sorted_category_expenses(transactions_in_the_date_range))
    list_key_1 = list(sorted_receipts(transactions_in_the_date_range))
    transactions_sorted = {
        "expenses": {
            "total_amount": separation_of_expenses(transactions_in_the_date_range),
            "main": [
                {
                    "category": list_key[i],
                    "amount": int(sorted_category_expenses(transactions_in_the_date_range).get(list_key[i])),
                }
                for i in range(len(list_key))
            ],
            "transfers_and_cash": [
                {
                    "category": "Наличные",
                    "amount": sorted_category_expenses(transactions_in_the_date_range).get("Наличные"),
                },
                {
                    "category": "Переводы",
                    "amount": sorted_category_expenses(transactions_in_the_date_range).get("Переводы"),
                },
            ],
        },
        "income": {
            "total_amount": separation_of_receipts(transactions),
            "main": [
                {
                    "category": list_key_1[i],
                    "amount": int(sorted_receipts(transactions_in_the_date_range).get(list_key_1[i])),
                }
                for i in range(len(list_key_1))
            ],
            "currency_rates": currency(symbols),
            "stock_prices": stock_prices(list_stock),
        },
    }
    logger.debug("Получен словарь с операциями в диапазоне дат по категориям")

    return transactions_sorted
