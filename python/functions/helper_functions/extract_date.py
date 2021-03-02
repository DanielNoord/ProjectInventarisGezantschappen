import datetime
import locale
import re


def extract_date(date_string, localization):
    """Returns a string containing the written date based on localization.
        (tries to) Handles missing data correctly

    Args:
        date_string (string): The date string in formate xxxx-xx-xx/xxxx-xx-xx
        localization (string): [description]

    Returns:
        date1 (string): The first date in text
        date2 (string): The second date in text
    """
    locale.setlocale(locale.LC_ALL, localization)
    date_pattern = re.compile(
        r"(\w{4})?-?(\w{2})?-?(\w{2})?/?(\w{4})?-?(\w{2})?-?(\w{2})?$"
    )
    y_1, m_1, d_1, y_2, m_2, d_2 = re.match(date_pattern, date_string).groups()
    if y_1:
        if m_1:
            if d_1:
                date1 = datetime.date(int(y_1), int(m_1), int(d_1)).strftime("%d %B %Y")
            else:
                date1 = datetime.date(int(y_1), int(m_1), 1).strftime("%B %Y")
        else:
            date1 = y_1
    else:
        date1 = None
    if y_2:
        if m_2:
            if d_2:
                date2 = datetime.date(int(y_2), int(m_2), int(d_2)).strftime("%d %B %Y")
            else:
                date2 = datetime.date(int(y_2), int(m_2), 1).strftime("%B %Y")
        else:
            date2 = y_2
    else:
        date2 = None
    return date1, date2
