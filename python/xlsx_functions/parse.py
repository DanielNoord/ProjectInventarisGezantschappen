#!/usr/bin/env python3

import re
from datetime import date
from warnings import warn

from date_functions import check_date_earlier, check_date_later
from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


def parse_volume(vol: tuple[Cell, ...]) -> tuple[str, str, str]:
    """Parses volumes. Note that current .xlsx files do not contain volume description.

    Args:
        vol: Volume to be parsed

    Returns:
        str: Number of the volume
        str: Title of the volume
        str: Date of the volume in the format xxxx-xx-xx/xxxx-xx-xx
    """
    if not isinstance(vol[0].value, (str)):
        raise ValueError("Volume number should be a string")
    vol_num = re.findall(r"ms(.*?)_.*", vol[0].value)[0]
    vol_title = f"Questo è il volume {vol_num}"
    vol_date = "2020-01-01/2020-12-31"
    return vol_num, vol_title, vol_date


def parse_dossier(  # pylint: disable=too-many-branches
    sheet: Worksheet,
    dos_number: str,
    vol_num: str,
    start_cell: Cell,
) -> tuple[str, str, str]:
    """Parses a dossier from a .xlsx sheet

    Args:
        sheet (Worksheet): Sheet with data
        dos_number (str): Number of the dossier
        vol_num (str): Number of the volume
        start_cell (Cell): Starting cell of the dossier

    Returns:
        str: Number of the dossier
        str: Title of the dossier
        str: Date of the dossier in the format xxxx-xx-xx/xxxx-xx-xx
    """
    ## Find highest page number in dossier
    for row_num in range(sheet.max_row, 1, -1):
        if i := sheet["A"][row_num - 1].value:
            if i.startswith(f"ms{vol_num}_{dos_number}"):
                dos_pages_match = re.search(r"ms.*?_.*?_(.*)", i)
                if dos_pages_match:
                    dos_pages = dos_pages_match.groups()[0]
                    break
                raise ValueError(
                    f"Can't parse the dossier pages of {dos_number} in {vol_num}"
                )

    ## Parse title from dossier title row
    if not isinstance(start_cell.value, str):
        raise ValueError(
            f"Number Cell of dossier should be a string. Incorrect for:\n{start_cell.value}"
        )
    if start_cell.value.endswith("_0") and start_cell.row:
        dos_title = sheet["B"][int(start_cell.row) - 1].value
    else:
        dos_title = "Missing dossier title"
        warn(f"Vol: {vol_num} Dos: {dos_number} is missing a dossier title")

    ## Find earliest and latest data
    early_date: tuple[str, str, str] = ("2020", "12", "31")
    late_date: tuple[str, str, str] = ("0", "0", "0")

    # Check if any of dates is "better"
    for row in sheet.iter_rows():
        if (
            not isinstance(row, tuple)
            or not isinstance(row[0], Cell)
            or isinstance(row[0].value, date)
        ):
            raise ValueError("Unrecognizable row type in {vol_num}")
        if row[0].value:
            if not isinstance(row[0].value, str):
                raise ValueError(
                    f"Expected the file number Cell to be a string. Incorrect for:\n{row[0].value}"
                )
            if row[0].value.startswith(f"ms{vol_num}_{dos_number}"):
                early_date = check_date_earlier(early_date, row)
                late_date = check_date_later(late_date, row)

    # Check for no changes and sanitization
    early_date_final: tuple[str, ...] = early_date
    late_date_final: tuple[str, ...] = late_date
    if early_date == ("2020", "12", "31"):
        early_date_final = ()
    if late_date == ("0", "0", "0"):
        late_date_final = ()
    if early_date[1] == "None" and early_date[2] != "None":
        early_date_final = tuple(early_date[0])
    if late_date[1] == "None" and late_date[2] != "None":
        late_date_final = tuple(late_date[0])
    early_date_final = tuple(str(i).zfill(2) for i in early_date_final if i != "None")
    late_date_final = tuple(str(i).zfill(2) for i in late_date_final if i != "None")
    dos_data = "/".join(["-".join(early_date_final), "-".join(late_date_final)])

    return dos_pages, dos_title, dos_data


def parse_file(row: tuple[Cell, ...]) -> tuple[str, str, str, str]:
    """Parse the data of a file row in .xlsx format

    Args:
        row (tuple[Cell, ...]): Row with file data in openpyxl Cell format

    Returns:
        str: Page number of the file
        str: Title of the file
        str: Place of the file
        str: Date of the file in the format xxxx-xx-xx
    """
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
    file_date = [str(row[2].value), str(row[3].value), str(row[4].value)]
    if file_date[1] == "None" and file_date[2] != "None":
        file_date[2] = "None"
    if file_date[1] == "None" and file_date[2] != "None":
        file_date[2] = "None"
    file_date = [i.zfill(2) for i in file_date if i != "None"]
    file_date_string = "-".join(file_date)
    return file_page, file_title, file_place, file_date_string
