from datetime import date

from openpyxl.cell.cell import Cell


def check_date_earlier(
    early_date: tuple[str | int | None, str | int | None, str | int | None],
    row: tuple[Cell, ...],
) -> tuple[str | float | None, str | float | None, str | float | None]:
    """Check if the given date is earlier than other data.

    Args:
        early_date: Strings of year, month, day
        row: .xlsx row with date info

    Returns:
        tuple[str, str, str]: Strings or ints of year, month, day
    """
    if (
        isinstance(row[2].value, date)
        or isinstance(row[3].value, date)
        or isinstance(row[4].value, date)
    ):
        raise ValueError(f"Excel cells should not be dates. Please check {row}")
    if not row[2].value or (early_date[0] is not None and int(row[2].value) > int(early_date[0])):
        return early_date
    if early_date[0] is not None and int(row[2].value) < int(early_date[0]):
        return row[2].value, row[3].value, row[4].value
    if not row[3].value or (early_date[1] is not None and int(row[3].value) > int(early_date[1])):
        return early_date
    if early_date[1] is not None and int(row[3].value) < int(early_date[1]):
        return row[2].value, row[3].value, row[4].value
    if not row[4].value or (early_date[2] is not None and int(row[4].value) > int(early_date[2])):
        return early_date
    if early_date[2] is not None and int(row[4].value) < int(early_date[2]):
        return row[2].value, row[3].value, row[4].value
    return early_date


def check_date_later(
    late_date: tuple[str | int | None, str | int | None, str | int | None],
    row: tuple[Cell, ...],
) -> tuple[str | float | None, str | float | None, str | float | None]:
    """Check if the given date is later than other data.

    Args:
        late_date: Strings of year, month, day
        row: .xlsx row with date info

    Returns:
        tuple[str, str, str]: Strings of year, month, day
    """
    if (
        isinstance(row[2].value, date)
        or isinstance(row[3].value, date)
        or isinstance(row[4].value, date)
    ):
        raise ValueError(f"Excel cells should not be dates. Please check {row}")
    if not row[2].value or (late_date[0] is not None and int(row[2].value) < int(late_date[0])):
        return late_date
    if late_date[0] is not None and int(row[2].value) > int(late_date[0]):
        return row[2].value, row[3].value, row[4].value
    if not row[3].value or (late_date[1] is not None and int(row[3].value) < int(late_date[1])):
        return late_date
    if late_date[1] is not None and int(row[3].value) > int(late_date[1]):
        return row[2].value, row[3].value, row[4].value
    if not row[4].value or (late_date[2] is not None and int(row[4].value) < int(late_date[2])):
        return late_date
    if late_date[2] is not None and int(row[4].value) > int(late_date[2]):
        return row[2].value, row[3].value, row[4].value
    return late_date
