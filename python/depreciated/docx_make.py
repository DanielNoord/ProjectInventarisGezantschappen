#!/usr/bin/env python3

import docx
from create_data import used_functions_and_titles, used_names
from functions.docx_make import list_to_be_translated, list_with_style


def create_to_be_translated(input_file):
    """Creates .docx file with all functions and titles to be translated
    Likely unnecessary in future

    Args:
        input_file (str): Name of "database" file with all relevant titles and functions
    """
    functions, titles = used_functions_and_titles(input_file)

    list_to_be_translated(functions, "Functions")
    list_to_be_translated(titles, "Titles")


def create_names_in_fondo(input_file):
    """Creates .docx file with all names mentioned in "fondo" file
    Adds a possible identifier for each entry
    Likely unnecessary in future

    Args:
        input_file (str): Name of "fondo" file with all relevant names/entries
    """
    doc = docx.Document(input_file)
    all_text = []
    for para in doc.paragraphs:
        if para.text.startswith("•"):
            all_text.append(para.text[2:])
    all_text = sorted(list(set(all_text)))
    list_with_style(all_text, "PeopleInFondo.docx")


def create_names(localization, input_file):
    """Creates a number of .docx files based on "database" file.

    Args:
        localization (str): Localization of output_files ("nl_NL", "it_IT", "en_GB")
        input_file (str): Name of "database" file
    """
    full_names = used_names(input_file)
    functions, titles = used_functions_and_titles(input_file)

    list_with_style(full_names, f"Namenlijst_{localization}")
    list_with_style(functions, f"Functielijst_{localization}")
    list_with_style(titles, f"Titellijst_{localization}")


if __name__ == "__main__":
    create_names("nl_NL", "inputs/Individuals.json")
    # create_to_be_translated("inputs/Individuals.json")
    # create_names_in_fondo("inputs/Fondo Legazione Paesi Bassi.docx")
    print("Done!")
