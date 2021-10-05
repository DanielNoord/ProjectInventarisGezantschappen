from datetime import date
from typing import Optional, Tuple

from openpyxl.cell.cell import Cell


def create_document_date(
    row: Tuple[Cell, ...], file_name: str
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    """Creates and checks a documents date info from a document row"""
    year, month, day = row[2].value, row[3].value, row[4].value
    if day and not month:
        raise ValueError(
            f"Document has day but no month, see: {file_name} row: {row[0].row}"
        )
    if day and not year:
        raise ValueError(
            f"Document has day but no year, see: {file_name} row: {row[0].row}"
        )
    if month and not year:
        raise ValueError(
            f"Document has month but no year, see: {file_name} row: {row[0].row}"
        )
    if any(isinstance(i, date) for i in (year, month, day)):
        raise TypeError(
            f"Some argument of document date isn't an integer, see: {file_name} row: {row[0].row}"
        )
    try:
        if year:
            year_final: Optional[int] = int(year)  # type: ignore # Can't be date
        else:
            year_final = None
        if month:
            month_final: Optional[int] = int(month)  # type: ignore
        else:
            month_final = None
        if day:
            day_final: Optional[int] = int(day)  # type: ignore
        else:
            day_final = None
    except ValueError as error:
        raise ValueError(
            f"Incorrect date format: {error}, see {file_name} row: {row[0].row}"
        ) from error
    return (year_final, month_final, day_final)
