from typing import NamedTuple, Optional


class SeriesData(NamedTuple):
    """Data about a series."""

    num: str
    title: str
    date: str
    level: int


class DateData(NamedTuple):
    """Dates formatted in the different languages (month names)."""

    date1_it: Optional[str]
    date2_it: Optional[str]
    date1_en: Optional[str]
    date2_en: Optional[str]
    date1_nl: Optional[str]
    date2_nl: Optional[str]


class FileData(NamedTuple):
    """Data about a file."""

    page: str
    title: str
    place: str
    date_string: str
    file_name: str
    series: str
    series_level: int
    authors: list[str]
    receivers: list[str]
    others: list[str]
    only_recto: bool
    only_verso: bool


class DateTuple(NamedTuple):
    """Tuple with entry for year, month and day."""

    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
