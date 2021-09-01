#!/usr/bin/env python3

from typing import Union

import openpyxl


def check_date_earlier(
    early_date: tuple[int, int, int],
    row: tuple[openpyxl.cell.cell.Cell],
) -> tuple[
    Union[int, str], Union[int, str], Union[int, str]
]:  # pylint: disable=too-many-return-statements
    """Check if the given date is earlier than other data

    Args:
        early_date (tuple[int, int, int]): Strings of year, month, day
        row (tuple[, int, int]): .xlsx row with date info

    Returns:
        tuple[Union[int, str], Union[int, str], Union[int, str]]: Strings or ints of year, month, day
    """
    if not row[2].value or int(row[2].value) > early_date[0]:
        return early_date
    if int(row[2].value) < early_date[0]:
        return (row[2].value, row[3].value, row[4].value)
    if not row[3].value or int(row[3].value) > early_date[1]:
        return early_date
    if int(row[3].value) < early_date[1]:
        return (row[2].value, row[3].value, row[4].value)
    if not row[4].value or int(row[4].value) > early_date[2]:
        return early_date
    if int(row[4].value) < early_date[2]:
        return (row[2].value, row[3].value, row[4].value)
    return early_date


def check_date_later(
    late_date: tuple[int, int, int],
    row: tuple[openpyxl.cell.cell.Cell],
) -> tuple[
    Union[int, str], Union[int, str], Union[int, str]
]:  # pylint: disable=too-many-return-statements
    """Check if the given date is later than other data

    Args:
        late_date (tuple[int, int, int]): Strings of year, month, day
        row (tuple[openpyxl.cell.cell.Cell],): .xlsx row with date info

    Returns:
        tuple[Union[int, str], Union[int, str], Union[int, str]]: Strings of year, month, day
    """
    if not row[2].value or int(row[2].value) < late_date[0]:
        return late_date
    if int(row[2].value) > late_date[0]:
        return (row[2].value, row[3].value, row[4].value)
    if not row[3].value or int(row[3].value) < late_date[1]:
        return late_date
    if int(row[3].value) > late_date[1]:
        return (row[2].value, row[3].value, row[4].value)
    if not row[4].value or int(row[4].value) < late_date[2]:
        return late_date
    if int(row[4].value) > late_date[2]:
        return (row[2].value, row[3].value, row[4].value)
    return late_date
