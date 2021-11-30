import re

from date_functions import check_date_for_missing_elements
from openpyxl.cell.cell import Cell
from typing_utils import FileData, SeriesData


def parse_series(serie: tuple[Cell, ...]) -> SeriesData:
    """Parses series. Note that current .xlsx files often do not contain series description"""
    if not isinstance(serie[0].value, (str)):
        raise ValueError(f"Series number should be a string, check {serie[0].value}")
    serie_num = re.findall(r"ms(\w+_)*(\w+?)_title", serie[0].value)[0][1]
    if (title := str(serie[1].value)) == "None":
        with open("outputs/missing_titles", "a", encoding="utf-8") as file:
            print(f"|Vol: {serie[0].value}|Missing a series title", file=file)
    vol_date = f"{serie[2].value or ''}/{serie[3].value or ''}"
    if level_string_match := re.match(fr".*{serie_num}_", serie[0].value):
        level_string = level_string_match.group()
    else:
        raise ValueError(f"Can't parse the series string: {serie[0].value}")
    return SeriesData(serie_num, title, vol_date, level_string.count("_"))


def parse_file(row: tuple[Cell, ...]) -> FileData:
    """Parse the data of a file row in .xlsx format"""
    if len(row) < 6:
        raise ValueError(
            f"Expected the row in Excel to have 6 cells. In correct for:\n{row}"
        )
    if not isinstance(row[0].value, str):
        raise ValueError(
            f"Expected Cell of file number to be a string. Incorrect for:\n{row[0].value}"
        )
    if mat := re.match(r"(.*)_(.*)", row[0].value):
        file_dossier = mat.groups()[0]
        file_page = mat.groups()[1]
    else:
        raise ValueError(f"Can't parse file number of:\n{row[0].value}")
    file_title = str(row[1].value)
    file_place = str(row[5].value)

    # Sanitize date
    check_date_for_missing_elements(
        row[2].value, row[3].value, row[4].value, row[0].value
    )
    file_date = [str(row[2].value), str(row[3].value), str(row[4].value)]
    if file_date[1] == "None" and file_date[2] != "None":
        file_date[2] = "None"
    if file_date[1] == "None" and file_date[2] != "None":
        file_date[2] = "None"
    file_date = [i.zfill(2) for i in file_date if i != "None"]
    file_date_string = "-".join(file_date)
    return FileData(
        file_page,
        file_title,
        file_place,
        file_date_string,
        row[0].value.replace("ms", "MS"),
        file_dossier,
        str(row[0].value).count("_") + 1,
    )
