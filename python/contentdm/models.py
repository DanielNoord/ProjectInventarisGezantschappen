from __future__ import annotations

import re
from dataclasses import dataclass

from data_parsing import control_title
from openpyxl.cell.cell import Cell
from typing_utils.translations_classes import Database
from xml_functions.title_elements import fill_in_name, fix_quotes


def _date(year: int | None, month: int | None, day: int | None) -> str:
    """The date in the format xxxx-xx-xx."""
    if month and not year:
        month = None
    if day and not month:
        day = None
    return "-".join(str(i).zfill(2) for i in (year, month, day) if i)


def _translate_title(title: str, date: str, database: Database) -> tuple[str, str, str]:
    """Translate a title into Dutch, English and Italian."""
    # Find document translation
    for pattern, trans in database.document_titles.items():
        if pattern.match(title):
            try:
                title_en = re.sub(pattern, trans["en_GB"], title)
                title_nl = re.sub(pattern, trans["nl_NL"], title)
                break
            except re.error as error:
                raise re.error(f"At {pattern} found the following error: {error}") from error
    else:
        raise ValueError(f"Could not find a translation for {title}")

    title_it = fill_in_name(title, database, date, "it_IT")
    title_en = fill_in_name(title_en, database, date, "en_GB")
    title_nl = fill_in_name(title_nl, database, date, "nl_NL")
    # Add and check italics
    if sum("_" in i for i in (title_it, title_en, title_nl)) == 1:
        raise ValueError(f"Only one language has italtics indication for {title}")

    if re.search(r"\"|“|”", title_it):
        title_it = fix_quotes(title_it)
        title_en = fix_quotes(title_en)
        title_nl = fix_quotes(title_nl)

    control_title(title_it, title)
    control_title(title_en, title)
    control_title(title_nl, title)

    return title_nl, title_en, title_it


@dataclass
class FileRow:
    scans: list[str]
    file_id: str
    series_id: str
    title: str
    title_en: str
    title_nl: str
    title_it: str
    year: int | None
    month: int | None
    day: int | None
    location: str | None
    authors: list[str]
    recipients: list[str]
    subjects: list[str]

    @classmethod
    def from_row(cls, row: tuple[Cell, ...], scans: list[str], database: Database) -> FileRow:
        # Check for empty lines, title lines or incorrect lines
        file_id = row[0].value
        if file_id is None:
            file_id = ""
        assert isinstance(file_id, str)
        if not file_id or file_id.endswith("_title") or " " in file_id:
            raise ValueError(f"Invalid file number '{file_id}'.")

        # Get series ID
        if mat := re.match(r"(.*)_(.*)", file_id):
            series_id = mat.groups()[0]
        else:
            raise ValueError(f"Can't parse series ID of: '{file_id}'")

        # Cast all rows to their expected type
        title = str(row[2].value) if row[2].value is not None else None
        year = int(row[3].value) if row[3].value is not None else None  # type: ignore[arg-type]
        month = int(row[4].value) if row[4].value is not None else None  # type: ignore[arg-type]
        day = int(row[5].value) if row[5].value is not None else None  # type: ignore[arg-type]
        location = str(row[6].value) if row[6].value is not None else None
        authors = str(row[7].value) if row[7].value is not None else None
        recipients = str(row[8].value) if row[8].value is not None else None
        subjects = str(row[9].value) if row[9].value is not None else None

        assert title, "Title should not be None here"
        title_nl, title_en, title_it = _translate_title(title, _date(year, month, day), database)

        return cls(
            scans=scans,
            file_id=file_id,
            series_id=series_id,
            title=title,
            title_en=title_en,
            title_nl=title_nl,
            title_it=title_it,
            year=year,
            month=month,
            day=day,
            location=location,
            authors=authors.split("; ") if authors else [],
            recipients=recipients.split("; ") if recipients else [],
            subjects=subjects.split("; ") if subjects else [],
        )


@dataclass
class SeriesRow:
    series_id: str
    title: str
    title_en: str
    title_nl: str
    title_it: str
    start: int
    end: int

    @classmethod
    def from_row(cls, row: tuple[Cell, ...], database: Database) -> SeriesRow:
        # Check for empty lines, title lines or incorrect lines
        series_id = row[0].value
        assert isinstance(series_id, str)
        series_id = series_id.removesuffix("_title")

        title = row[2].value
        assert isinstance(title, str) and title

        # Cast all rows to their expected type
        start = int(row[3].value) if row[3].value is not None else None  # type: ignore[arg-type]
        end = int(row[4].value) if row[4].value is not None else None  # type: ignore[arg-type]

        title_nl, title_en, title_it = _translate_title(title, _date(start, None, None), database)

        return cls(
            series_id=series_id,
            title=title,
            title_en=title_en,
            title_nl=title_nl,
            title_it=title_it,
            start=start,
            end=end,
        )
