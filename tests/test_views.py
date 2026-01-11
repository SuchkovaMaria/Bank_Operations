from unittest.mock import patch

from src.views import sorting_events


@patch("src.views.currency")
@patch("src.views.stock_prices")
def test_sorting_events_1(mock_stock_prices, mock_currency, views_test_1):
    mock_currency.return_value = [{"currency": "EUR", "rate": 92.24}]
    mock_stock_prices.return_value = [{"stock": "GOOGL", "price": 328.57}]
    assert sorting_events("2020-06-20") == views_test_1
