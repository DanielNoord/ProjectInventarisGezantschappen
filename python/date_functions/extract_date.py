import datetime
import re
from typing import Literal

from babel.dates import format_date
from typing_utils import DateData


def extract_date(
    date_string: str, localization: Literal["it_IT", "nl_NL", "en_GB"]
) -> tuple[str | None, str | None]:
    """Returns a string containing the written date based on localization.

        (tries to) Handles missing data correctly

    Args:
        date_string: The date string in formate xxxx-xx-xx/xxxx-xx-xx
        localization: Localization abbreviation

    Returns:
        date1_string: The first date in text
        date2_string: The second date in text
    """
    date_pattern = re.compile(r"^(\w{4})?-?(\w{2})?-?(\w{2})?/?(\w{4})?-?(\w{2})?-?(\w{2})?$")
    if mat := re.match(date_pattern, date_string):
        y_1, m_1, d_1, y_2, m_2, d_2 = mat.groups()
    else:
        raise ValueError(f"Can't parse the following date string:\n{date_string}")

    date1_datetime: datetime.date | None = None
    date2_datetime: datetime.date | None = None
    date1_string: str | None = None
    date2_string: str | None = None

    if y_1:
        if m_1:
            if d_1:
                date1_datetime = datetime.date(int(y_1), int(m_1), int(d_1))
                date1_string = format_date(date1_datetime, "d MMMM yyyy", locale=localization)
            else:
                date1_datetime = datetime.date(int(y_1), int(m_1), 1)
                date1_string = format_date(date1_datetime, "MMMM yyyy", locale=localization)
        else:
            date1_datetime = datetime.date(int(y_1), 1, 1)
            date1_string = y_1

    if y_2:
        if m_2:
            if d_2:
                date2_datetime = datetime.date(int(y_2), int(m_2), int(d_2))
                date2_string = format_date(date2_datetime, "d MMMM yyyy", locale=localization)
            else:
                date2_datetime = datetime.date(int(y_2), int(m_2), 1)
                date2_string = format_date(date2_datetime, "MMMM yyyy", locale=localization)
        else:
            date2_datetime = datetime.date(int(y_2), 1, 1)
            date2_string = y_2

    # Make sure that date1 comes before date2
    if date1_datetime and date2_datetime:
        if date1_datetime > date2_datetime:
            raise ValueError(f"The first date in {date_string} comes before the second date")

    return date1_string, date2_string


def create_date_data(date: str) -> DateData:
    """Create a DateData tuple by calling the extract_date for all localizations."""
    date1_it, date2_it = extract_date(date, "it_IT")
    date1_en, date2_en = extract_date(date, "en_GB")
    date1_nl, date2_nl = extract_date(date, "nl_NL")
    return DateData(date1_it, date2_it, date1_en, date2_en, date1_nl, date2_nl)
