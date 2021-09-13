#!/usr/bin/env python3


from typing import Optional


def check_begin(  # pylint: disable=too-many-return-statements
    date: tuple[Optional[int], Optional[int], Optional[int]], begin_date: list[str]
) -> bool:
    """Checks if a date falls after or on a specific date

    Args:
        date (tuple[Optional[int], Optional[int], Optional[int]]): Date to check
        begin_date (list[str]): Begin date where the other date has to be after or on

    Returns:
        bool: Whether the check passed
    """
    if begin_date == [""]:
        return True
    if date[0] is not None and date[0] > int(begin_date[0]):
        return True
    if date[0] is not None and date[0] == int(begin_date[0]):
        if date[1] is not None and len(begin_date) > 1:
            if date[1] > int(begin_date[1]):
                return True
            if date[1] == int(begin_date[1]):
                if date[2] is not None and len(begin_date) > 2:
                    return bool(date[2] >= int(begin_date[2]))
                return True
            return False
        return True
    return False


def check_end(  # pylint: disable=too-many-return-statements
    date: tuple[Optional[int], Optional[int], Optional[int]], end_date: list[str]
) -> bool:
    """Checks if a date falls before or on a specific date

    Args:
        date (tuple[Optional[int], Optional[int], Optional[int]]): Date to check
        end_date (list[str]): End date where the other date has to be before or on

    Returns:
        bool: Whether the check passed
    """
    if end_date == [""]:
        return True
    if date[0] is not None and (date[0] < int(end_date[0])):
        return True
    if date[0] is not None and date[0] == int(end_date[0]):
        if date[1] is not None and len(end_date) > 1:
            if date[1] < int(end_date[1]):
                return True
            if date[1] == int(end_date[1]):
                if date[2] is not None and len(end_date) > 2:
                    return bool(date[2] <= int(end_date[2]))
                return True
            return False
        return True
    return False


def check_date(
    date: tuple[Optional[int], Optional[int], Optional[int]], function_period: str
) -> bool:
    """Checks if the given date falls within the period an individual held the position

    Args:
        date (tuple[Optional[int], Optional[int], Optional[int]]): Date of the file to be checked
        function_period (str): Period in which an individual held a position

    Returns:
        bool: Whether the date fits or not
    """
    begin_date, end_date = [i.split("-") for i in function_period.split("/")]
    if check_begin(date, begin_date) and check_end(date, end_date):
        return True
    return False
