#!/usr/bin/env python3


def check_begin(date, begin_date):  # pylint: disable=too-many-return-statements
    """Checks if a date falls after or on a specific date

    Args:
        date (list): Date to check
        begin_date (list): Begin date where the other date has to be after or on

    Returns:
        bool: Whether the check passed
    """
    if begin_date == [""]:
        return True
    if date[0] > int(begin_date[0]):
        return True
    if date[0] == int(begin_date[0]):
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


def check_end(date, end_date):  # pylint: disable=too-many-return-statements
    """Checks if a date falls before or on a specific date

    Args:
        date (list): Date to check
        end_date (list): End date where the other date has to be before or on

    Returns:
        bool: Whether the check passed
    """
    if end_date == [""]:
        return True
    if date[0] < int(end_date[0]):
        return True
    if date[0] == int(end_date[0]):
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


def check_date(date, function_period):
    """Checks if the given date falls within the period an individual held the position

    Args:
        date (list): Date of the file to be checked
        function_period (str): Period in which an individual held a position

    Returns:
        bool: Whether the date fits or not
    """
    begin_date, end_date = [i.split("-") for i in function_period.split("/")]
    if check_begin(date, begin_date) and check_end(date, end_date):
        return True
    return False
