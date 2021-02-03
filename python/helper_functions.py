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
    y1, m1, d1, y2, m2, d2 = re.match(date_pattern, date_string).groups()
    # Date 1
    if y1:
        if m1:
            if d1:
                date1 = datetime.date(int(y1), int(m1), int(d1)).strftime("%d %B %Y")
            else:
                date1 = Mdate(int(y1), int(m1)).strftime("%B %Y")
        else:
            date1 = y1
    else:
        date1 = None
    # Date 2
    if y2:
        if m2:
            if d2:
                date2 = datetime.date(int(y2), int(m2), int(d2)).strftime("%d %B %Y")
            else:
                date2 = Mdate(int(y2), int(m2)).strftime("%B %Y")
        else:
            date2 = y2
    else:
        date2 = None
    return date1, date2