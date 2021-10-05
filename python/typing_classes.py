from typing import NamedTuple, Optional


class VolData(NamedTuple):
    num: str
    title_it: str
    title_en: str
    title_nl: str
    date: str


class DateData(NamedTuple):
    date1_it: Optional[str]
    date2_it: Optional[str]
    date1_en: Optional[str]
    date2_en: Optional[str]
    date1_nl: Optional[str]
    date2_nl: Optional[str]
