import jdatetime
from datetime import datetime

JALALI_MONTHS_FA = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

JALALI_MONTHS_EN = [
    "Farvardin", "Ordibehesht", "Khordad", "Tir", "Mordad", "Shahrivar",
    "Mehr", "Aban", "Azar", "Dey", "Bahman", "Esfand"
]

class PersianDateTime:
    """
    A utility class for converting Gregorian dates to Persian dates.
    """
    def convert(self, gregorian_date_str: str, lang: str = 'fa') -> str:
        """
        Converts a Gregorian date string to a formatted Persian date string.

        Args:
            gregorian_date_str: The input Gregorian date in "YYYY-MM-DD" format.
            lang: The language for the month name. 'fa' for Persian (default),
                  'en' for English.

        Returns:
            The formatted Persian date string (e.g., "8 شهریور 1404").
            Returns an error message if the date format is incorrect or the
            language is not supported.
        """
        if lang not in ['fa', 'en']:
            raise ValueError("Language not supported. Use 'fa' or 'en'.")

        try:
            gregorian_date = datetime.strptime(gregorian_date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Error: Invalid date format. Please use YYYY-MM-DD."

        persian_date = jdatetime.date.fromgregorian(date=gregorian_date)

        day = persian_date.day
        year = persian_date.year
        month = persian_date.month

        if lang == 'fa':
            month_name = JALALI_MONTHS_FA[month - 1]
        else: # lang == 'en'
            month_name = JALALI_MONTHS_EN[month - 1]

        return f"{day} {month_name} {year}"
