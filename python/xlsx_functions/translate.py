#!/usr/bin/env python3

import os
import re
from typing import Literal, Pattern

from openpyxl import load_workbook
from openpyxl.styles import Font
from typing_utils import (
    TranslationDictCleaned,
    TranslationDictCleanedDocuments,
    TranslationDictCleanedTitles,
)


def translate_xlsx(  # pylint: disable=too-many-arguments
    directory_name: str,
    file_name: str,
    localization: Literal["nl_NL", "en_GB"],
    translations: TranslationDictCleanedDocuments,
    translation_data: tuple[
        TranslationDictCleanedTitles, TranslationDictCleaned, TranslationDictCleaned
    ],
    used_translations: set[Pattern],
) -> None:
    """Translate .xlsx file

    Args:
        directory_name (str): Directory of .xlsx file
        file_name (str): Name of .xlsx file
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation
        translations: Translations of common document titles
        translation_data: Dictionaries with translation data for titles, functions and places
        used_translations (set[Pattern]): Used translations
    """
    workbook = load_workbook(f"{directory_name}/{file_name}")
    for row in workbook[workbook.sheetnames[0]].iter_rows():
        # Translate title
        if row[1].value is not None:
            line = row[1].value

            # Check if line matches one of the patterns that are automatically translated
            for pattern, trans in translations.items():
                if pattern.match(line):
                    line = re.sub(pattern, trans[localization], line)
                    used_translations.add(pattern)
                    break
            else:
                row[1].font = Font(color="00008b")
                # Print out unrecognized lines
                print(f"Did not find translation for:\n{row[0].value}: {line}")
            row[1].value = line

        # Translate title
        if row[5].value is not None:
            place = row[5].value
            if place in translation_data[2].keys():
                place = translation_data[2][place][localization]
            else:
                row[5].font = Font(color="00008b")
                print(f"Did not find placename: {place}")
            row[5].value = place

    new_directory = (
        directory_name.replace("inputs", "outputs")
        .replace("VolumesExcelSanitized/", "VolumesExcelTranslated/")
        .replace("it_IT", f"{localization}")
    )
    os.makedirs(
        os.path.join(os.getcwd(), new_directory),
        exist_ok=True,
    )
    workbook.save(f"{new_directory}/{file_name.replace('it_IT', localization)}")
    print(f"File written to {new_directory}/{file_name.replace('it_IT', localization)}")
