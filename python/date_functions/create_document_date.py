from date_functions.check_date_for_missing import check_date_for_missing_elements
from openpyxl.cell.cell import Cell
from typing_utils import DateTuple


def create_document_date(row: tuple[Cell, ...], file_name: str) -> DateTuple:
    """Creates and checks a documents date info from a document row."""
    year, month, day = row[2].value, row[3].value, row[4].value
    check_date_for_missing_elements(year, month, day, row[0].value)
    try:
        if year:
            year_final: int | None = int(year)  # type: ignore[arg-type] # Can't be date
        else:
            year_final = None
        if month:
            month_final: int | None = int(month)  # type: ignore[arg-type]
        else:
            month_final = None
        if day:
            day_final: int | None = int(day)  # type: ignore[arg-type]
        else:
            day_final = None
    except ValueError as error:
        raise ValueError(
            f"Incorrect date format: {error}, see {file_name} row: {row[0].row}"
        ) from error
    return DateTuple(year_final, month_final, day_final)
