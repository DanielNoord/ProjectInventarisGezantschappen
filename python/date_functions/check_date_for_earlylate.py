#!/usr/bin/env python3

from datetime import date

from openpyxl.cell.cell import Cell


def check_date_earlier(  # pylint: disable=too-many-return-statements
    early_date: tuple[str, str, str],
    row: tuple[Cell, ...],
) -> tuple[str, str, str]:
    """Check if the given date is earlier than other data

    Args:
        early_date (tuple[str, str, str]): Strings of year, month, day
        row (tuple[Cell, ...]): .xlsx row with date info

    Returns:
        tuple[str, str, str]: Strings or ints of year, month, day
    """
    if (
        isinstance(row[2].value, date)
        or isinstance(row[3].value, date)
        or isinstance(row[4].value, date)
    ):
        raise ValueError(f"Excel cells should not be dates. Please check {row}")
    if not row[2].value or int(row[2].value) > int(early_date[0]):
        return early_date
    if int(row[2].value) < int(early_date[0]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    if not row[3].value or int(row[3].value) > int(early_date[1]):
        return early_date
    if int(row[3].value) < int(early_date[1]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    if not row[4].value or int(row[4].value) > int(early_date[2]):
        return early_date
    if int(row[4].value) < int(early_date[2]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    return early_date


def check_date_later(  # pylint: disable=too-many-return-statements
    late_date: tuple[str, str, str],
    row: tuple[Cell, ...],
) -> tuple[str, str, str]:
    """Check if the given date is later than other data

    Args:
        late_date (tuple[str, str, str]): Strings of year, month, day
        row (tuple[Cell, ...]): .xlsx row with date info

    Returns:
        tuple[str, str, str]: Strings of year, month, day
    """
    if (
        isinstance(row[2].value, date)
        or isinstance(row[3].value, date)
        or isinstance(row[4].value, date)
    ):
        raise ValueError(f"Excel cells should not be dates. Please check {row}")
    if not row[2].value or int(row[2].value) < int(late_date[0]):
        return late_date
    if int(row[2].value) > int(late_date[0]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    if not row[3].value or int(row[3].value) < int(late_date[1]):
        return late_date
    if int(row[3].value) > int(late_date[1]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    if not row[4].value or int(row[4].value) < int(late_date[2]):
        return late_date
    if int(row[4].value) > int(late_date[2]):
        return str(row[2].value), str(row[3].value), str(row[4].value)
    return late_date
