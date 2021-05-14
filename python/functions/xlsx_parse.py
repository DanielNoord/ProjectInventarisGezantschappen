#!/usr/bin/env python3

import re
from warnings import warn

from functions.helper_functions.check_date_for_earlylate import check_date_earlier, check_date_later


def parse_volume(vol):
    """Parses volumes. Note that current .xlsx files do not contain volume description.

    Args:
        vol (str): Volume to be parsed

    Returns:
        str: Number of the volume
        str: Title of the volume
        str: Date of the volume in the format xxxx-xx-xx/xxxx-xx-xx
    """
    vol_num = re.findall(r"ms(.*?)_.*", vol[0].value)[0]
    vol_title = f"Questo è il volume {vol_num}"
    vol_date = "2020-01-01/2020-12-31"
    return vol_num, vol_title, vol_date


def parse_dossier(sheet, dos_number, vol_num, start_cell):
    """Parses a dossier from a .xlsx sheet

    Args:
        sheet (openpyxl.worksheet.worksheet.Worksheet): Sheet with data
        dos_number (str): Number of the dossier
        vol_num (str): Number of the volume
        start_cell (openpyxl.cell.cell.Cell): Starting cell of the dossier

    Returns:
        str: Number of the dossier
        str: Title of the dossier
        str: Date of the dossier in the format xxxx-xx-xx/xxxx-xx-xx
    """
    ## Find highest page number in dossier
    for row_num in range(sheet.max_row, 1, -1):
        if i := sheet["A"][row_num - 1].value:
            if i.startswith(f"ms{vol_num}_{dos_number}"):
                dos_pages = re.search(r"ms.*?_.*?_(.*)", i).groups()[0]
                break

    ## Parse title from dossier title row
    if start_cell.value.endswith("_0"):
        dos_title = sheet["B"][start_cell.row - 1].value
    else:
        dos_title = "Missing dossier title"
        warn(f"Vol: {vol_num} Dos: {dos_number} is missing a dossier title")

    ## Find earliest and latest data
    early_date = [2020, 12, 31]
    late_date = [0, 0, 0]

    # Check if any of dates is "better"
    for row in sheet.iter_rows():
        if row[0].value and row[0].value.startswith(f"ms{vol_num}_{dos_number}"):
            early_date = check_date_earlier(early_date, row)
            late_date = check_date_later(late_date, row)

    # Check for no changes and sanitization
    if early_date == [2020, 12, 31]:
        early_date = []
    if late_date == [0, 0, 0]:
        late_date = []
    if early_date[1] is None and early_date[2] is not None:
        early_date[2] = None
    if late_date[1] is None and late_date[2] is not None:
        late_date[2] = None
    early_date = [str(i).zfill(2) for i in early_date if i is not None]
    late_date = [str(i).zfill(2) for i in late_date if i is not None]
    dos_data = "/".join(["-".join(early_date), "-".join(late_date)])

    return dos_pages, dos_title, dos_data


def parse_file(input_file):
    """Parse the data of a file row in .xlsx format

    Args:
        input_file (tuple): Row with file data in openpyxl Cell format

    Returns:
        str: Page number of the file
        str: Title of the file
        str: Place of the file
        str: Date of the file in the format xxxx-xx-xx
    """
    file_page = re.match(r".*_(.*)", input_file[0].value).groups()[0]
    file_title = input_file[1].value
    file_place = input_file[5].value

    # Sanitize date
    date = [input_file[2].value, input_file[3].value, input_file[4].value]
    if date[1] is None and date[2] is not None:
        date[2] = None
    if date[1] is None and date[2] is not None:
        date[2] = None
    date = [str(i).zfill(2) for i in date if i is not None]
    file_date = "-".join(date)
    return file_page, file_title, file_place, file_date
