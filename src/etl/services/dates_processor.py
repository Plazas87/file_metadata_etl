"""Dates prcessor module."""
import logging
from datetime import datetime, timedelta
from typing import List

logger = logging.getLogger(__name__)


class DatesProcessor:
    """DatesProcessor class."""

    _date_format: str

    def __init__(self, date_format: str) -> None:
        """Class constructor."""
        self._date_format = date_format

    def process(self, initial_date: str, end_date: str) -> List[str]:
        """
        Process the date interval and return a list of directory names.".

        Args:
            initial_date (str): initial date
            end_date (str): end date

        Returns:
            List[str]: list of dates between in the format: 20230101AM or 20230101PM
        """
        initial_date = self._to_datetime(date=initial_date)
        end_date = self._to_datetime(date=end_date)

        dates_between: List[str] = []
        # Calculate the difference between dates
        date_difference = (end_date - initial_date).days

        # Generate the list of dates
        date_list = [initial_date + timedelta(days=i) for i in range(date_difference + 1)]

        for date in date_list:
            day = self._format_integers(number=date.day)
            month = self._format_integers(number=date.month)

            for zz in ["AM", "PM"]:
                date_str = f"{date.year}{month}{day}{zz}"
                dates_between.append(date_str)

        return dates_between

    def _format_integers(self, number: int) -> str:
        """
        Return a zero-padded decimal number.

        Args:
            number (int): integer

        Returns:
            str: zero-padded decimal number
        """
        return str(number) if number >= 10 else f"0{number}"

    def _to_datetime(self, date: str) -> datetime:
        """Transfor the date from string to a datetime object."""
        try:
            processed_date = datetime.strptime(date, self._date_format)

        except Exception as err:
            logger.error("Please check date format: '%s'", str(err))
            raise Exception from err

        return processed_date

