from unittest.mock import patch

from src.utils import (currency, reading_operations_xlsx, separation_of_expenses, separation_of_receipts,
                       sorted_category_expenses, sorted_receipts, stock_prices)


@patch("requests.get")
def test_currency_1(mock_response, currency_test_1, currency_test_2):
    mock_response.return_value.json.return_value = currency_test_1
    assert currency("USD, EUR") == currency_test_2


@patch("requests.get")
def test_currency_2(mock_response, currency_test_3):
    mock_response.return_value.json.return_value = currency_test_3
    assert currency("ghg") == []


@patch("finnhub.Client")
def test_stock_prices_1(mock_stock, stock_price_test_1):
    mock_stock.return_value.quote.return_value = {"c": 259.37}
    assert stock_prices(["AAPL"]) == stock_price_test_1


def test_reading_operations_xlsx(reading_operations_xlsx_test_1):
    assert reading_operations_xlsx().head(3).fillna(0).to_dict() == reading_operations_xlsx_test_1


def test_separation_of_expenses(df_test_1):
    assert separation_of_expenses(df_test_1) == 15599


def test_sorted_category_expenses(df_test_1, sorted_category_expenses_test_1):
    assert sorted_category_expenses(df_test_1) == sorted_category_expenses_test_1


def test_separation_of_receipts(df_test_1):
    assert separation_of_receipts(df_test_1) == 2300


def test_sorted_receipts(df_test_1):
    assert sorted_receipts(df_test_1) == {"Бонусы": 2300}
