#!/usr/bin/env python3

import os
import re
from typing import Literal

from data_parsing import name_string
from openpyxl import load_workbook
from typing_utils import TranslationDictCleaned, TranslationDictCleanedTitles


def fill_in_xlsx(
    directory_name: str,
    file_name: str,
    individuals: dict,
    translations: tuple[
        TranslationDictCleanedTitles, TranslationDictCleaned, TranslationDictCleaned
    ],
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> None:
    """Fills an individual volume .xlsx file

    Args:
        directory_name (str): Name of input directory
        file_name (str): Name of input file
        individuals (dict): Dictionary of all individuals based on inputs/Individuals.json
        translations: Dictionaries with translation data for titles, functions and places
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation
    """
    workbook = load_workbook(f"{directory_name}/{file_name}")
    for row in workbook[workbook.sheetnames[0]].iter_rows():
        if row[1].value is not None:
            date = (int(row[2].value), int(row[3].value), int(row[4].value))
            line = re.split(r"( |\.|,|\(|\))", row[1].value)
            for index, word in enumerate(line):
                if word.startswith("$"):
                    line[index] = name_string(
                        individuals[word], date, translations, localization
                    )
            line_str = "".join(line)

            # Clean up string
            line_str = line_str[0].upper() + line_str[1:]
            line_str = line_str.replace("{", "(").replace("}", ")")
            row[1].value = line_str

    new_directory = (
        directory_name.replace("VolumesExcelSanitized/", "VolumesExcelFinal/")
        .replace("VolumesExcelTranslated/", "VolumesExcelFinal/")
        .replace("inputs", "outputs")
    )
    os.makedirs(
        os.path.join(os.getcwd(), new_directory),
        exist_ok=True,
    )
    workbook.save(f"{new_directory}/{file_name}")
    print(f"File written to {new_directory}/{file_name}")
