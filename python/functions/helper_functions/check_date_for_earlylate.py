def check_date_earlier(early_date, row):  # pylint: disable=too-many-return-statements
    """Check if the given date is earlier than other data

    Args:
        early_date (list): Strings of year, month, day
        row (row): .xlsx row with date info

    Returns:
        list: Strings of year, month, day
    """
    if not row[2].value or int(row[2].value) > int(early_date[0]):
        return early_date
    if int(row[2].value) < int(early_date[0]):
        return [row[2].value, row[3].value, row[4].value]
    if not row[3].value or int(row[3].value) > int(early_date[1]):
        return early_date
    if int(row[3].value) < int(early_date[1]):
        return [row[2].value, row[3].value, row[4].value]
    if not row[4].value or int(row[4].value) > int(early_date[2]):
        return early_date
    if int(row[4].value) < int(early_date[2]):
        return [row[2].value, row[3].value, row[4].value]
    return early_date


def check_date_later(late_date, row):  # pylint: disable=too-many-return-statements
    """Check if the given date is later than other data

    Args:
        late_date (list): Strings of year, month, day
        row (row): .xlsx row with date info

    Returns:
        list: Strings of year, month, day
    """
    if not row[2].value or int(row[2].value) < int(late_date[0]):
        return late_date
    if int(row[2].value) > int(late_date[0]):
        return [row[2].value, row[3].value, row[4].value]
    if not row[3].value or int(row[3].value) < int(late_date[1]):
        return late_date
    if int(row[3].value) > int(late_date[1]):
        return [row[2].value, row[3].value, row[4].value]
    if not row[4].value or int(row[4].value) < int(late_date[2]):
        return late_date
    if int(row[4].value) > int(late_date[2]):
        return [row[2].value, row[3].value, row[4].value]
    return late_date
