#!/usr/bin/env python3

import datetime
import locale
import re
from typing import Literal, Optional


def extract_date(  # pylint: disable=too-many-branches
    date_string: str, localization: Literal["it_IT", "nl_NL", "en_GB"]
) -> tuple[Optional[str], Optional[str]]:
    """Returns a string containing the written date based on localization.
        (tries to) Handles missing data correctly

    Args:
        date_string (str): The date string in formate xxxx-xx-xx/xxxx-xx-xx
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation

    Returns:
        date1_string (str): The first date in text
        date2_string (str): The second date in text
    """
    locale.setlocale(locale.LC_ALL, f"{localization}.UTF-8")
    date_pattern = re.compile(
        r"^(\w{4})?-?(\w{2})?-?(\w{2})?/?(\w{4})?-?(\w{2})?-?(\w{2})?$"
    )
    if mat := re.match(date_pattern, date_string):
        y_1, m_1, d_1, y_2, m_2, d_2 = mat.groups()
    else:
        raise ValueError(f"Can't parse the following date string:\n{date_string}")

    date1_datetime: Optional[datetime.date] = None
    date2_datetime: Optional[datetime.date] = None
    date1_string: Optional[str] = None
    date2_string: Optional[str] = None

    if y_1:
        if m_1:
            if d_1:
                date1_datetime = datetime.date(int(y_1), int(m_1), int(d_1))
                date1_string = date1_datetime.strftime("%d %B %Y")
            else:
                date1_datetime = datetime.date(int(y_1), int(m_1), 1)
                date1_string = date1_datetime.strftime("%B %Y")
        else:
            date1_datetime = datetime.date(int(y_1), 1, 1)
            date1_string = y_1

    if y_2:
        if m_2:
            if d_2:
                date2_datetime = datetime.date(int(y_2), int(m_2), int(d_2))
                date2_string = date2_datetime.strftime("%d %B %Y")
            else:
                date2_datetime = datetime.date(int(y_2), int(m_2), 1)
                date2_string = date2_datetime.strftime("%B %Y")
        else:
            date2_datetime = datetime.date(int(y_2), 1, 1)
            date2_string = y_2

    # Make sure that date1 comes before date2
    if date1_datetime and date2_datetime:
        if date1_datetime > date2_datetime:
            raise ValueError(
                f"The first date in {date_string} comes before the second date"
            )

    return date1_string, date2_string