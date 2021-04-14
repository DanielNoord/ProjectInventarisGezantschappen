import json
import os
import re

from openpyxl import Workbook, load_workbook

from functions.create_name_string import name_string
from functions.translate import initialize_translation_database
from functions.xlsx_translate import translate_xlsx


def fill_in_xlsx(directory_name, file_name, individuals, translations, localization):
    """Translates and writes an individual volume .xlsx file

    Args:
        directory_name (str): Name of input directory
        file_name (str): Name of input file
        individuals (dict): Dictionary of all individuals based on inputs/Individuals.json
        translations (list): Dictionaries of function and title translations
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")
    """
    workbook = load_workbook(f"{directory_name}/{file_name}")
    for row in workbook[workbook.sheetnames[0]].iter_rows():
        if row[1].value is not None:
            date = [row[2].value, row[3].value, row[4].value]
            line = re.split(r"( |\.|,|\(|\))", row[1].value)
            for index, word in enumerate(line):
                if word.startswith("$"):
                    line[index] = name_string(
                        individuals[word], date, translations, localization
                    )
            line = "".join(line)

            # Clean up string
            if line[-1] in [" ", ",", "."]:  # Remove final characters
                line = line[:-1]
            line = line[0].upper() + line[1:]
            line = line.replace("( ", "(").replace(" )", ")")
            row[1].value = line

    new_directory = directory_name.replace(
        "VolumesExcel/", "VolumesExcelFilled/Final_"
    ).replace("inputs", "outputs")
    os.makedirs(
        os.path.join(os.getcwd(), new_directory),
        exist_ok=True,
    )
    workbook.save(f"{new_directory}/Final_{file_name}")
    print(f"File written to {new_directory}/Final_{file_name}")


def create_filled_xlsx(directory_name, localization):
    """Creates the .xlsx files of all volumes in the input directory

    Args:
        directory_name (str): Name of the directory with the input .xlsx files
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")
    """
    with open("inputs/Individuals.json") as file:
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
                i for i in load_workbook(f"{directory_names[0]}/{filename}").active.rows
            ]
            rows_it = [
                i
                for i in load_workbook(
                    f"{directory_names[1]}/{filename.replace('.xlsx', '')}_it_IT.xlsx"
                ).active.rows
            ]
            rows_en = [
                i
                for i in load_workbook(
                    f"{directory_names[2]}/{filename.replace('.xlsx', '')}_en_GB.xlsx"
                ).active.rows
            ]
            rows_nl = [
                i
                for i in load_workbook(
                    f"{directory_names[3]}/{filename.replace('.xlsx', '')}_nl_NL.xlsx"
                ).active.rows
            ]
            for index, row in enumerate(rows_original):
                new_sheet.append(tuple(i.value for i in row))
                new_sheet.append(tuple(i.value for i in rows_it[index]))
                new_sheet.append(tuple(i.value for i in rows_en[index]))
                new_sheet.append(tuple(i.value for i in rows_nl[index]))
            os.makedirs(
                os.path.join(os.getcwd(), "inputs/VolumesExcel"),
                exist_ok=True,
            )
            new_file.save(f"outputs/VolumesExcel/Control_{filename}")
            print(f"Wrote file to outputs/VolumesExcel/Control_{filename}")


def create_translated_xlsx(directory_name, localization):
    """Creates the .xlsx files with a number of easy translation already done

    Args:
        directory_name (str): Name of the directory with the input .xlsx files
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")
    """
    with open("inputs/Translations/DocumentTitles.json") as file:
        translations = json.load(file)
    del translations["$schema"]

    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        if not str(file).count("~$") and str(file).startswith("b'Paesi"):
            filename = os.fsdecode(file)
            translate_xlsx(directory_name, filename, localization, translations)


if __name__ == "__main__":
    # create_filled_xlsx("inputs/VolumesExcel/en_GB", "en_GB")
    create_filled_xlsx("inputs/VolumesExcel/it_IT", "it_IT")
    # create_filled_xlsx("inputs/VolumesExcel/nl_NL", "nl_NL")
    create_translated_xlsx("inputs/VolumesExcel/it_IT", "en_GB")
    create_translated_xlsx("inputs/VolumesExcel/it_IT", "nl_NL")
    """create_xlsx_controle(
        [
            "inputs/VolumesExcel/original",
            "inputs/VolumesExcel/it_IT",
            "inputs/VolumesExcel/en_GB",
            "inputs/VolumesExcel/nl_NL",
        ]
    )"""
