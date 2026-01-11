import json

from src.reports import expenses_by_category
from src.services import search_by_description_and_category
from src.utils import reading_operations_xlsx
from src.views import sorting_events


def main():
    while True:
        users_input_1 = input(
            "Программа: Привет! Добро пожаловать в программу работы\n"
            "по сортировке операций.\n"
            "Доступные функции:\n"
            "1. Вывод популярных категориям расходов и категории доходов\n"
            "2. Поиск операции\n"
            "3. Отчет по расходам за последние 3 месяца\n"
        )

        if users_input_1 == "1":
            print("Укажите период выполнения операций")
            print("Дата окончания периода:")
            users_input_selected_date_year = input("Укажите год (четыре цифры)\n")
            users_input_selected_date_month = input("Укажите месяц (две цифры)\n")
            users_input_selected_date_day = input("Укажите день (две цифры)\n")
            selected_date = "-".join(
                [users_input_selected_date_year, users_input_selected_date_month, users_input_selected_date_day]
            )
            users_input_1_1 = input("Указать начало периода? Да/Нет\n").lower()
            if users_input_1_1 == "да":
                users_input_start_date_year = input("Укажите год (четыре цифры)\n")
                users_input_start_date_month = input("Укажите месяц (две цифры)\n")
                users_input_start_date_day = input("Укажите день (две цифры)\n")
                start_date = "-".join(
                    [users_input_start_date_year, users_input_start_date_month, users_input_start_date_day]
                )
                transactions = sorting_events(selected_date, start_date)
            else:
                transactions = sorting_events(selected_date)
            operations = json.dumps(transactions, ensure_ascii=False)
            print(operations)
            break

        elif users_input_1 == "2":
            users_input_word = input("Введите слово для поиска операций\n")
            operations = search_by_description_and_category(users_input_word)
            print(operations)
            break

        elif users_input_1 == "3":
            transactions = reading_operations_xlsx()
            users_input_optional_date = input("Указать дату окончания периода? Да/Нет\n").lower()
            if users_input_optional_date == "да":
                users_input_optional_date_year = input("Укажите год (четыре цифры)\n")
                users_input_optional_date_month = input("Укажите месяц (две цифры)\n")
                users_input_optional_date_day = input("Укажите день (две цифры)\n")
                optional_date = "-".join(
                    [users_input_optional_date_year, users_input_optional_date_month, users_input_optional_date_day]
                )
                users_input_category = input("Введите категорию расходов\n").capitalize()
                operations = expenses_by_category(transactions, users_input_category, optional_date)
            else:
                users_input_category = input("Введите категорию расходов\n").capitalize()
                operations = expenses_by_category(transactions, users_input_category)
            if isinstance(operations, str) == False:
                operations = operations.to_json(orient="records", force_ascii=False)
                print(type(operations))

            print(operations)
            break


if __name__ == "__main__":
    main()
