from typing import NamedTuple, Optional


class VolData(NamedTuple):
    """Data about a volume"""

    num: str
    title: str
    date: str


class DateData(NamedTuple):
    """Dates formatted in the different languages (month names)"""

    date1_it: Optional[str]
    date2_it: Optional[str]
    date1_en: Optional[str]
    date2_en: Optional[str]
    date1_nl: Optional[str]
    date2_nl: Optional[str]


class FileData(NamedTuple):
    """Data about a file"""

    page: str
    title: str
    place: str
    date_string: str
    file_name: str


class DateTuple(NamedTuple):
    """Tuple with entry for year, month and day"""

    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
