from src.services import search_by_description_and_category


def test_search_by_description_and_category(masseg_test_1):
    assert search_by_description_and_category("Таня") == "[]"
    assert search_by_description_and_category("Азер Г.") == str(masseg_test_1)
