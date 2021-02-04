import re
import locale
import datetime

class Mdate(datetime.date):
    """ A datetime.date where day doesn't matter. """

    def __new__(cls, year, month):
        """Python calls __new__ instead of __init__ for immutable objects."""
        return super().__new__(cls, year, month, 1)

    def __repr__(self):
        """Because you're implementing __new__ you also need __repr__ or else you get
        TypeError: __new__() takes 3 positional arguments but 4 were given."""
        return '{0}({1}, {2}, 1)'.format(self.__class__.__name__, self.year, self.month)

    def __reduce__(self):
        """You need __reduce__ to support pickling."""
        return (self.__class__, (self.year, self.month))


def extract_date(date_string, localization):
    locale.setlocale(locale.LC_ALL, localization)
    date_pattern = re.compile(r"(\w{4})?-?(\w{2})?-?(\w{2})?/?(\w{4})?-?(\w{2})?-?(\w{2})?$")
    y_1, m_1, d_1, y_2, m_2, d_2 = re.match(date_pattern, date_string).groups()
    if y_1:
        if m_1:
            if d_1:
                date1 = datetime.date(int(y_1), int(m_1), int(d_1)).strftime("%d %B %Y")
            else:
                date1 = Mdate(int(y_1), int(m_1)).strftime("%B %Y")
        else:
            date1 = y_1
    else:
        date1 = None
    if y_2:
        if m_2:
            if d_2:
                date2 = datetime.date(int(y_2), int(m_2), int(d_2)).strftime("%d %B %Y")
            else:
                date2 = Mdate(int(y_2), int(m_2)).strftime("%B %Y")
        else:
            date2 = y_2
    else:
        date2 = None
    return date1, date2
