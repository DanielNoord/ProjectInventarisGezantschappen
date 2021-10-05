#!/usr/bin/env python3

import os
import re

from openpyxl import load_workbook


def sanitize_xlsx(directory_name: str, file_name: str) -> None:
    """Sanitize an .xlsx file

    Args:
        directory_name (str): Directory of .xlsx file
        file_name (str): Name of .xlsx file
    """
    last_line = 0
    workbook = load_workbook(f"{directory_name}/{file_name}")
    for row in workbook[workbook.sheetnames[0]].iter_rows():
        for index, cell in enumerate(row):
            if cell.value is not None:
                # # Check document number for inconsistensies
                # if index == 0:
                #     if not cell.value.startswith("ms"):
                #         raise Exception(f"Incorrect document number: {cell.value}")
                #     document_num = re.match(r"(.*_)+(.*)", cell.value).groups()[-1]
                #     if (
                #         document_num == str(last_line + 1)
                #         or document_num == f"{last_line}bis"
                #         or document_num in ["0", "1"]
                #         or "-" in document_num
                #     ):
                #         if "-" in document_num:
                #             last_line = 0
                #         elif not document_num.endswith("bis"):
                #             last_line = int(document_num)
                #     else:
                #         print(cell.value)
                #         last_line = int(document_num)

                # Clean up string
                line = cell.value
                if isinstance(line, str) and line.isspace():
                    line = ""
                elif isinstance(line, str):
                    if line[-1] in {" ", ",", ".", ";"}:  # Remove final characters
                        line = line[:-1]
                    if line[0] in {" "}:  # Remove spaces in first place
                        line = line[1:]
                    if index != 0:
                        line = line[0].upper() + line[1:]
                    line = line.replace("( ", "(").replace(" )", ")").replace("  ", " ")
                row[index].value = line

    new_directory = directory_name.replace("inputs", "outputs").replace(
        "VolumesExcel/", "VolumesExcelSanitized/"
    )
    os.makedirs(
        os.path.join(os.getcwd(), new_directory),
        exist_ok=True,
    )
    workbook.save(f"{new_directory}/{file_name}")
    print(f"File written to {new_directory}/{file_name}")
