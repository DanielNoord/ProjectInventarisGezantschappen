import os
from pathlib import Path

from openpyxl import load_workbook
from xlsx_functions.helper_functions import compare_rows, is_partial_match
from xlsx_make import create_sanitized_xlsx


# pylint: disable-next=unused-argument
def find_partial_matches(print_to_file: bool, sanitize: bool) -> None:
    """Find all rows that are partial matches."""
    input_dir = Path("inputs") / "VolumesExcel" / "it_IT"
    if sanitize:
        create_sanitized_xlsx(str(input_dir))
    sanitized_dir = (
        str(input_dir)
        .replace("inputs", "outputs")
        .replace("VolumesExcel", "VolumesExcelSanitized")
    )
    files = [i for i in os.listdir(sanitized_dir) if i.startswith("Paesi")]
    count = 0
    count_all = 0
    for file in sorted(
        files,
        key=lambda name: int(
            name.replace("Paesi Bassi VOLUME ", "").replace("_it_IT.xlsx", "")
        ),
    ):
        workbook = load_workbook(Path(sanitized_dir) / file)
        first_sheet = workbook[workbook.sheetnames[0]]

        prev_row = None
        for row in first_sheet.iter_rows():
            count_all += 1
            if prev_row is None:
                prev_row = row
                continue

            if not compare_rows(prev_row, row) and is_partial_match(prev_row, row):
                count += 1
                print("Prev row:")
                print(" ".join([str(i.value) for i in prev_row]))
                print("Row:")
                print(" ".join([str(i.value) for i in row]))
            prev_row = row
    print(count)
    print(count_all)
