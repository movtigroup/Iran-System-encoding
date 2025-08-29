import pytest
from iran_encoding.utils.date import PersianDateTime

def test_persian_date_time_conversion_fa():
    pdt = PersianDateTime()
    gregorian_date = "2025-08-30"
    persian_date = pdt.convert(gregorian_date, lang='fa')
    assert persian_date == "8 شهریور 1404"

def test_persian_date_time_conversion_en():
    pdt = PersianDateTime()
    gregorian_date = "2025-08-30"
    persian_date = pdt.convert(gregorian_date, lang='en')
    assert persian_date == "8 Shahrivar 1404"

def test_invalid_date_format():
    pdt = PersianDateTime()
    gregorian_date = "2025/08/30"
    error_message = pdt.convert(gregorian_date)
    assert "Invalid date format" in error_message

def test_unsupported_language():
    pdt = PersianDateTime()
    gregorian_date = "2025-08-30"
    with pytest.raises(ValueError, match="Language not supported"):
        pdt.convert(gregorian_date, lang='es')
