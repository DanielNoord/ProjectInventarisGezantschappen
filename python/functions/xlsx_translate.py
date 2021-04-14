# pylint: disable=W0123
import os
import re

from openpyxl import load_workbook
from openpyxl.styles import Font


def translate_xlsx(directory_name, file_name, localization, translations):
    """Translate .xlsx file

    Args:
        directory_name (str): Directory of .xlsx file
        file_name (str): Name of .xlsx file
        localization (str): Localization string of target language
        translations (dict): Translations of common document titles
    """
    workbook = load_workbook(f"{directory_name}/{file_name}")
    for row in workbook[workbook.sheetnames[0]].iter_rows():
        if row[1].value is not None:
            line = row[1].value
            if (mat := re.match(r"Lettera (di|del) (\$\w*) (a|al) (\$\w*)$", line)) :
                line = eval(
                    translations["Lettera (di|del) (n1) (a|al) (n2)$"][localization]
                )(mat.groups()[1], mat.groups()[3])
            elif (mat := re.match(r"Lettera (di|del) (\$\w*)$", line)) :
                line = eval(translations["Lettera (di|del) (n1)$"][localization])(
                    mat.groups()[1]
                )
            elif (
                mat := re.match(
                    r"Lettera circolare (di|del) (\$\w*) (a|al) (\$\w*)$", line
                )
            ) :
                line = eval(
                    translations["Lettera circolare (di|del) (n1) (a|al) (n2)$"][
                        localization
                    ]
                )(mat.groups()[1], mat.groups()[3])
            elif (mat := re.match(r"Lettera circolare (di|del) (\$\w*)$", line)) :
                line = eval(
                    translations["Lettera circolare (di|del) (n1)$"][localization]
                )(mat.groups()[1])
            elif (mat := re.match(r"Minuta di lettera (a|al) (\$\w*)$", line)) :
                line = eval(
                    translations["Minuta di lettera (a|al) (n1)$"][localization]
                )(mat.groups()[1])
            elif (mat := re.match(r"Minuta di lettera inviata (a|al) (\$\w*)$", line)) :
                line = eval(
                    translations["Minuta di lettera inviata (a|al) (n1)$"][localization]
                )(mat.groups()[1])
            elif (mat := re.match(r"Minuta di lettera (di|del) (\$\w*)$", line)) :
                line = eval(
                    translations["Minuta di lettera (di|del) (n1)$"][localization]
                )(mat.groups()[1])
            elif (
                mat := re.match(
                    r"Minuta di lettera (di|del) (\$\w*) (a|al) (\$\w*)$", line
                )
            ) :
                line = eval(
                    translations["Minuta di lettera (di|del) (n1) (a|al) (n2)$"][
                        localization
                    ]
                )(mat.groups()[1], mat.groups()[3])
            elif re.match(r"Minuta di lettera$", line):
                line = translations["Minuta di lettera$"][localization]
            elif re.match(r"Minuta di risposta$", line):
                line = translations["Minuta di risposta$"][localization]
            elif re.match(r"Nota di ricezione dei dispacci diplomatici$", line):
                line = translations["Nota di ricezione dei dispacci diplomatici$"][
                    localization
                ]
            elif re.match(r"Bianca$", line):
                line = translations["Bianca$"][localization]
            else:
                row[1].font = Font(color="FF0000")

            # Clean up string
            if line[-1] in [" ", ",", "."]:  # Remove final characters
                line = line[:-1]
            line = line[0].upper() + line[1:]
            line = line.replace("( ", "(").replace(" )", ")")
            row[1].value = line

    new_directory = (
        directory_name.replace("inputs", "outputs")
        .replace("VolumesExcel/", "VolumesExcelFilled/Translated_")
        .replace("it_IT", f"{localization}")
    )
    os.makedirs(
        os.path.join(os.getcwd(), new_directory),
        exist_ok=True,
    )
    workbook.save(f"{new_directory}/{file_name.replace('it_IT', localization)}")
    print(f"File written to {new_directory}/{file_name.replace('it_IT', localization)}")
