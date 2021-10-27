import re
from datetime import date
from typing import Union

from date_functions import (
    check_date_earlier,
    check_date_for_missing_elements,
    check_date_later,
)
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet
from typing_utils import FileData, VolData


def parse_volume(vol: tuple[Cell, ...]) -> VolData:
    """Parses volumes. Note that current .xlsx files do not contain volume description"""
    if not isinstance(vol[0].value, (str)):
        raise ValueError(f"Volume number should be a string, check {vol[0].value}")
    vol_num = re.findall(r"ms(.*?)_.*", vol[0].value)[0]
    title = str(vol[1].value)
    if title == "None":
        with open("outputs/missing_titles", "a", encoding="utf-8") as file:
            print(f"|Vol: {vol_num}|Missing a volume title", file=file)
    vol_date = f"{vol[2].value or ''}/{vol[3].value or ''}"
    return VolData(vol_num, title, vol_date)


def parse_dossier(  # pylint: disable=too-many-branches
    sheet: Worksheet,
    dos_number: str,
    vol_num: str,
    start_cell: Cell,
) -> tuple[str, str]:
    """Parses a dossier from a .xlsx sheet"""
    # No longer used, but kept for later
    # ## Find highest page number in dossier
    # for row_num in range(sheet.max_row, 1, -1):
    #     if i := sheet["A"][row_num - 1].value:
    #         if i.startswith(f"ms{vol_num}_{dos_number}"):
    #             dos_pages_match = re.search(r"ms.*?_.*?_(.*)", i)
    #             if dos_pages_match:
    #                 dos_pages = dos_pages_match.groups()[0]
    #                 break
    #             raise ValueError(
    #                 f"Can't parse the dossier pages of {dos_number} in {vol_num}"
    #             )

    ## Parse title from dossier title row
    if not isinstance(start_cell.value, str):
        raise ValueError(
            f"Number Cell of dossier should be a string. Incorrect for:\n{start_cell.value}"
        )
    if start_cell.value.endswith("_title") and start_cell.row:
        dos_title = str(sheet["B"][int(start_cell.row) - 1].value)
        if dos_title == "None":
            with open("outputs/missing_titles", "a", encoding="utf-8") as file:
                print(
                    f"|Vol: {vol_num} Dos: {dos_number} |Missing a dossier title",
                    file=file,
                )
    else:
        dos_title = "Missing dossier title"
        with open("outputs/missing_titles", "a", encoding="utf-8") as file:
            print(
                f"|Vol: {vol_num} Dos: {dos_number}|Missing a dossier title", file=file
            )

    ## Find earliest and latest data
    early_date: tuple[
        Union[str, int, None], Union[str, int, None], Union[str, int, None]
    ] = (
        "2020",
        "12",
        "31",
    )
    late_date: tuple[
        Union[str, int, None], Union[str, int, None], Union[str, int, None]
    ] = ("0", "0", "0")

    # Check if any of dates is "better"
    for row in sheet.iter_rows():
        if (
            not isinstance(row, tuple)
            or not isinstance(row[0], Cell)
            or isinstance(row[0].value, date)
        ):
            raise ValueError(f"Unrecognizable row type in {vol_num}")
        if row[0].value:
            if not isinstance(row[0].value, str):
                raise ValueError(
                    f"Expected the file number Cell to be a string. Incorrect for:\n{row[0].value}"
                )
            if row[0].value.startswith(f"ms{vol_num}_{dos_number}"):
                early_date = check_date_earlier(early_date, row)
                late_date = check_date_later(late_date, row)

    # Check for no changes and sanitization
    early_date_final: tuple[str, ...] = (
        str(early_date[0]),
        str(early_date[1]),
        str(early_date[2]),
    )
    late_date_final: tuple[str, ...] = (
        str(late_date[0]),
        str(late_date[1]),
        str(late_date[2]),
    )
    if early_date_final == ("2020", "12", "31"):
        early_date_final = ()
    elif early_date_final[1] == "None" and early_date_final[2] != "None":
        early_date_final = (early_date_final[0],)
    if late_date_final == ("0", "0", "0"):
        late_date_final = ()
    elif late_date_final[1] == "None" and late_date_final[2] != "None":
        late_date_final = (late_date_final[0],)
    early_date_final = tuple(str(i).zfill(2) for i in early_date_final if i != "None")
    late_date_final = tuple(str(i).zfill(2) for i in late_date_final if i != "None")
    dos_date = "/".join(["-".join(early_date_final), "-".join(late_date_final)])

    return dos_title, dos_date


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
    if mat := re.match(r".*_(.*)", row[0].value):
        file_page = mat.groups()[0]
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
    return FileData(file_page, file_title, file_place, file_date_string, row[0].value.replace("ms", "MS"))
