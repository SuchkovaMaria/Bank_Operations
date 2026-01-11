import json
import logging
import os
import re

from src.utils import reading_operations_xlsx

current_dir = os.path.dirname(__file__)
absolute_path = os.path.join(current_dir, "..")
os.chdir(absolute_path)
logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler_services = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8")
file_formatter_services = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler_services.setFormatter(file_formatter_services)
logger.addHandler(file_handler_services)


def search_by_description_and_category(word):
    """Функция поиска по описанию и категории операции"""

    transactions = reading_operations_xlsx()
    logger.debug("Прочитан файл")

    transactions_1 = transactions.fillna("")
    transactions_2 = transactions_1.to_dict(orient="records")
    logger.debug("Данные переведены в тип dict")

    transactions_list = []
    if word == "" or word == " ":
        print("неверное слово")
        transactions_list = []
    else:
        pattern = re.compile(rf"{word}", re.IGNORECASE)
        for dict_i in transactions_2:
            if pattern.search(dict_i.get("Категория", "")):
                transactions_list.append(dict_i)
            elif pattern.search(dict_i.get("Описание", "")):
                transactions_list.append(dict_i)
        if len(transactions_list) == 0:
            print("Операций не найдено")
            transactions_list = []
    transactions_json = json.dumps(transactions_list, ensure_ascii=False)
    logger.debug("Поиск завершен")

    return transactions_json
