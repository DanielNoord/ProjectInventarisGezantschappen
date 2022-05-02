from typing import Union

from date_functions.create_dates_tuple import create_date_tuple
from typing_utils import DateTuple


def check_begin(  # pylint: disable=too-many-return-statements
    date: DateTuple, begin_date: DateTuple
) -> bool:
    """Checks if a date falls after or on a specific date."""
    if not begin_date.year and not begin_date.month and not begin_date.day:
        return True
    if date.year and date.year > begin_date.year:  # type: ignore[operator]
        return True
    if date.year and date.year == begin_date.year:
        if date.month and begin_date.month:
            if date.month > begin_date.month:
                return True
            if date.month == begin_date.month:
                if date.day and begin_date.day:
                    return bool(date.day >= begin_date.day)
                return True
            return False
        return True
    return False


def check_end(  # pylint: disable=too-many-return-statements
    date: DateTuple, end_date: DateTuple
) -> bool:
    """Checks if a date falls before or on a specific date."""
    if not end_date.year and not end_date.month and not end_date.day:
        return True
    if date.year and date.year < end_date.year:  # type: ignore[operator]
        return True
    if date.year and date.year == end_date.year:
        if date.month and end_date.month:
            if date.month < end_date.month:
                return True
            if date.month == end_date.month:
                if date.day and end_date.day:
                    return bool(date.day <= end_date.day)
                return True
            return False
        return True
    return False


def check_date(
    date: Union[tuple[DateTuple], tuple[DateTuple, DateTuple]],
    function_period: str,
) -> bool:
    """Checks if the given date falls within the period an individual held the position."""
    dates = create_date_tuple(function_period)
    if len(dates) != 2:
        raise ValueError(f"Missing a '/' in function/title with date {function_period}")

    begin_date, end_date = dates  # type: ignore[misc]

    if len(date) == 1:
        if check_begin(date[0], begin_date) and check_end(date[0], end_date):
            return True
    elif check_begin(end_date, date[0]) and check_end(begin_date, date[1]):  # type: ignore[misc]
        return True
    return False
