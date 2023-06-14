from typing import NamedTuple


class SeriesData(NamedTuple):
    """Data about a series."""

    num: str
    title: str
    date: str
    level: int


class DateData(NamedTuple):
    """Dates formatted in the different languages (month names)."""

    date1_it: str | None
    date2_it: str | None
    date1_en: str | None
    date2_en: str | None
    date1_nl: str | None
    date2_nl: str | None


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

    year: int | None
    month: int | None
    day: int | None
