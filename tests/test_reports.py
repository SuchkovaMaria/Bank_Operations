from src.reports import expenses_by_category


def test_report_output_1(df_test_1, df_test_2):
    assert expenses_by_category(df_test_1, "Переводы", "2020-06-20") == df_test_2
    assert expenses_by_category(df_test_1, "", "2020-06-20") == "Операций не найдено"
