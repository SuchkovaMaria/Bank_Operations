import logging
import os
import warnings

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

API_KEY = os.environ.get("API_KEY")

current_dir = os.path.dirname(__file__)
absolute_path = os.path.join(current_dir, "..")
os.chdir(absolute_path)
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler_utils = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_formatter_utils = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler_utils.setFormatter(file_formatter_utils)
logger.addHandler(file_handler_utils)


def currency(symbols):
    """Функция определения курса валют"""

    try:
        base = "RUB"
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base={base}"

        payload = {}
        headers = {"apikey": os.getenv("API_KEY")}

        response = requests.get(url, headers=headers, data=payload)
        logger.debug("Получен ответ от API")
        currency_rates = []
        for key, value in response.json().get("rates").items():
            currency_rates.append({"currency": key, "rate": round(1 / value, 2)})
        logger.debug("Сформирован список курсов валют")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        currency_rates = []

    return currency_rates


def stock_prices(list_stock):
    """Функция определения стоимости акций"""

    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY_2"))
    logger.debug("Получен ответ от API")
    list_stocks_new = []
    for i in list_stock:
        quote = finnhub_client.quote(i)
        list_stocks_new.append({"stock": i, "price": quote["c"]})
    logger.debug("Сформирован список стоимости акций")
    return list_stocks_new


def reading_operations_xlsx():
    """Функция для считывания операций из файла .xlsx"""
    dir = os.getcwd()
    absolute_path = os.path.join(dir, "..")
    os.chdir(absolute_path)
    path_to_direct = os.path.dirname(__file__)
    path_to_file_1 = os.path.join(path_to_direct, "..", "data", "operations.xlsx")
    logger.debug("Определен путь до файла")

    excel_data = pd.read_excel(path_to_file_1)
    logger.debug("Прочитан файл")

    excel_data.fillna(0)
    operations = excel_data.sort_values(by="Сумма операции")
    logger.debug("Осуществлена сортировка по сумме операций")

    return operations


def separation_of_expenses(operations):
    """Функуия для подсчета общей суммы расходов"""

    operations_expenses_df = operations[operations["Сумма операции"] < 0]
    sum_of_expenses = round((operations_expenses_df["Сумма операции"].sum()) * (-1))
    return sum_of_expenses


def sorted_category_expenses(operations):
    """Функция группировки расходов по категориям"""

    operations_expenses_df = operations[operations["Сумма операции"] < 0]
    logger.debug("Отделены расходные операции")

    grop_expenses_df = round(operations_expenses_df.groupby("Категория")["Сумма операции"].sum().abs(), 0)
    logger.debug("Посчитаны суммы расходов по категориям")

    sort_expenses_df_1 = grop_expenses_df.sort_values(ascending=False).head(7)
    logger.debug("Определены 7 популярных категорий")

    rest_sum = grop_expenses_df.sort_values(ascending=False).iloc[7:].sum()

    grop_cash_expenses_df = (
        operations_expenses_df[operations_expenses_df["Категория"] == "Наличные"]["Сумма операции"].sum()
    ) * (-1)
    logger.debug("Определены расходы по категории - Наличные")

    grop_translation_expenses_df = (
        operations_expenses_df[operations_expenses_df["Категория"] == "Переводы"]["Сумма операции"].sum()
    ) * (-1)
    logger.debug("Определены расходы по категории - Переводы")

    list_categories = []
    list_categories.append(int(rest_sum))
    list_categories.append(int(grop_cash_expenses_df))
    list_categories.append(int(grop_translation_expenses_df))
    sort_expenses_df_2 = pd.Series(list_categories, index=["Остальное", "Наличные", "Переводы"])
    sort_expenses_df_3 = (pd.concat([sort_expenses_df_1, sort_expenses_df_2], axis=0)).to_dict()
    logger.debug("Сформирован список расходов по категориям (популярные, остальное, наличные, переводы)")

    return sort_expenses_df_3


def separation_of_receipts(operations):
    """Функуия для отделение доходов"""

    operations_receipts_df = operations[operations["Сумма операции"] > 0]
    logger.debug("Отделены доходные операции")

    sum_of_receipts = int(operations_receipts_df["Сумма операции"].sum())
    logger.debug("Посчитана сумма доходов")

    return sum_of_receipts


def sorted_receipts(operations):
    """Функция группировки доходов по категориям"""
    operations_receipts_df = operations[operations["Сумма операции"] > 0]
    logger.debug("Отделены доходные операции")

    grop_receipts_df = operations_receipts_df.groupby("Категория")["Сумма операции"].sum().abs()
    logger.debug("Посчитаны суммы доходов по категориям")

    sort_receipts_df_1 = grop_receipts_df.sort_values(ascending=False)
    sort_receipts_df_2 = sort_receipts_df_1.to_dict()
    logger.debug("Сформирован словарь по категориям доходов")

    return sort_receipts_df_2


def formation_df():
    """Функция для формирования DF"""
    data = [
        ["24.04.2020", -2063, "RUB", "Супермаркеты", "Магнит"],
        ["19.03.2020", -2159, "RUB", "Супермаркеты", "Пятерочка"],
        ["06.04.2020", -2055, "RUB", "Супермаркеты", "Магнит"],
        ["14.05.2020", -507, "RUB", "Транспорт", "Такси"],
        ["21.03.2020", -607, "RUB", "Транспорт", "Такси"],
        ["07.02.2020", -3500, "RUB", "Перевод", "Иванов Д."],
        ["24.05.2020", -708, "RUB", "Переводы", "Лютикова Л."],
        ["13.03.2020", -1500, "RUB", "Наличные", "Снятие с банкомата"],
        ["06.05.2020", -2500, "RUB", "Наличные", "Снятие с банкомата"],
        ["11.04.2020", 1500, "RUB", "Бонусы", "КЭШбэк"],
        ["21.02.2020", 800, "RUB", "Бонусы", "КЭШбэк"],
    ]
    df = pd.DataFrame(data, columns=["Дата платежа", "Сумма операции", "Валюта операции", "Категория", "Описание"])
    return df


if __name__ == "__main__":
    i = formation_df()
    m = sorted_receipts(i)
    print(m)
