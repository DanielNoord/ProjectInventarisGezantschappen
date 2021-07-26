#!/usr/bin/env python3

import json
import os
import re
import time

from openpyxl import Workbook, load_workbook

from functions.json_translate import initialize_translation_database
from functions.xlsx_fill_in_names import fill_in_xlsx
from functions.xlsx_sanitize import sanitize_xlsx
from functions.xlsx_translate import translate_xlsx


def create_filled_xlsx(directory_name, localization):
    """Creates the .xlsx files of all volumes in the input directory

    Args:
        directory_name (str): Name of the directory with the input .xlsx files
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")
    """
    with open("inputs/Individuals.json", encoding="utf-8") as file:
        individuals_data = json.load(file)
    del individuals_data["$schema"]
    translation_data = initialize_translation_database()

    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        if not str(file).count("~$") and str(file).startswith("b'Paesi"):
            filename = os.fsdecode(file)
            fill_in_xlsx(
                directory_name,
                filename,
                individuals_data,
                translation_data,
                localization,
            )


def create_xlsx_controle(directory_names):
    """Creates a combination of the various translated .xlsx files into one "control file"

    Args:
        directory_names (list): Directories of the file to be merged
    """
    directory = os.fsencode(directory_names[0])
    for file in os.listdir(directory):
        if not str(file).count("~$") and str(file).startswith("b'Paesi"):
            new_file = Workbook()
            new_sheet = new_file.active
            filename = os.fsdecode(file)
            rows_original = [
                i
                for i in load_workbook(  # pylint: disable=unnecessary-comprehension
                    f"{directory_names[0]}/{filename}"
                ).active.rows
            ]
            rows_it = [
                i
                for i in load_workbook(  # pylint: disable=unnecessary-comprehension
                    f"{directory_names[1]}/{filename.replace('.xlsx', '')}_it_IT.xlsx"
                ).active.rows
            ]
            rows_en = [
                i
                for i in load_workbook(  # pylint: disable=unnecessary-comprehension
                    f"{directory_names[2]}/{filename.replace('.xlsx', '')}_en_GB.xlsx"
                ).active.rows
            ]
            rows_nl = [
                i
                for i in load_workbook(  # pylint: disable=unnecessary-comprehension
                    f"{directory_names[3]}/{filename.replace('.xlsx', '')}_nl_NL.xlsx"
                ).active.rows
            ]
            for index, row in enumerate(rows_original):
                if row[0].value != rows_it[index][0].value:
                    raise Exception(
                        f"Difference in document number found for {row[0].value} in original"
                    )
                new_sheet.append(tuple(i.value for i in row))
                new_sheet.append(tuple(i.value for i in rows_it[index]))
                new_sheet.append(tuple(i.value for i in rows_en[index]))
                new_sheet.append(tuple(i.value for i in rows_nl[index]))
                new_sheet.append([])
            os.makedirs(
                os.path.join(os.getcwd(), "outputs/VolumesExcelControl"),
                exist_ok=True,
            )
            new_filename = f"Control_{filename}"
            new_file.save(f"outputs/VolumesExcelControl/{new_filename}")
            print(f"Wrote file to outputs/VolumesExcelControl/{new_filename}")


def create_translated_xlsx(directory_name, localization):
    """Creates the .xlsx files with a number of easy translation already done

    Args:
        directory_name (str): Name of the directory with the input .xlsx files
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")
    """
    with open("inputs/Translations/DocumentTitles.json", encoding="utf-8") as file:
        translations = json.loads(file.read())
    del translations["$schema"]
    translation_patterns = {re.compile(k): v for k, v in translations.items()}
    translation_data = initialize_translation_database()
    used_translations = set()

    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        if not str(file).count("~$") and str(file).startswith("b'Paesi"):
            filename = os.fsdecode(file)
            translate_xlsx(
                directory_name,
                filename,
                localization,
                translation_patterns,
                translation_data,
                used_translations,
            )
    unused_trans = [i for i in translation_patterns.keys() if i not in used_translations]
    print("Done!\nFound the following unused translations:\n", unused_trans)


def create_sanitized_xlsx(directory_name):
    """Creates the .xlsx files with a number of easy sanitizations

    Args:
        directory_name (str): Name of the directory with the input .xlsx files
    """

    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        if not str(file).count("~$") and str(file).startswith("b'Paesi"):
            filename = os.fsdecode(file)
            sanitize_xlsx(directory_name, filename)


def do_full_loop():
    """Completes the full process of input files till seperate translations and control file"""
    print("STARTING CREATION OF .XLSX DOCUMENTS\n")
    start_time = time.time()
    create_sanitized_xlsx("inputs/VolumesExcel/it_IT")
    create_translated_xlsx("outputs/VolumesExcelSanitized/it_IT", "en_GB")
    create_translated_xlsx("outputs/VolumesExcelSanitized/it_IT", "nl_NL")
    create_filled_xlsx("outputs/VolumesExcelTranslated/en_GB", "en_GB")
    create_filled_xlsx("outputs/VolumesExcelSanitized/it_IT", "it_IT")
    create_filled_xlsx("outputs/VolumesExcelTranslated/nl_NL", "nl_NL")
    create_xlsx_controle(
        [
            "inputs/VolumesExcel/original",
            "outputs/VolumesExcelFinal/it_IT",
            "outputs/VolumesExcelFinal/en_GB",
            "outputs/VolumesExcelFinal/nl_NL",
        ]
    )
    print(
        "\n\nFINISHED CREATING ALL .XLSX DOCUMENTS\n",
        f"Process took {time.time() - start_time:.03f} seconds",
    )


if __name__ == "__main__":
    dname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dname)

    # create_sanitized_xlsx("inputs/VolumesExcel/it_IT")
    # create_translated_xlsx("outputs/VolumesExcelSanitized/it_IT", "en_GB")
    # create_translated_xlsx("outputs/VolumesExcelSanitized/it_IT", "nl_NL")
    # create_filled_xlsx("outputs/VolumesExcelTranslated/en_GB", "en_GB")
    # create_filled_xlsx("outputs/VolumesExcelSanitized/it_IT", "it_IT")
    # create_filled_xlsx("outputs/VolumesExcelTranslated/nl_NL", "nl_NL")
    # create_xlsx_controle(
    #     [
    #         "inputs/VolumesExcel/original",
    #         "outputs/VolumesExcelFinal/it_IT",
    #         "outputs/VolumesExcelFinal/en_GB",
    #         "outputs/VolumesExcelFinal/nl_NL",
    #     ]
    # )
    do_full_loop()
