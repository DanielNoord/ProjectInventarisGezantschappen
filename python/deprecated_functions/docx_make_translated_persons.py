#!/usr/bin/env python3
# type: ignore # pylint: disable-all

from create_data import person_with_identifier
from docx_functions import list_of_translated_data, list_of_translated_data_with_style
from functions.docx_load import extract_persons_and_identifiers


def create_name_docx(input_file_names, input_file_data) -> None:
    """Creates a document with all names encountered in the input_file with translations
    in Italian, Dutch and English

    Args:
        input_file_names: Name of file with all people + their identifier
        input_file_data: Name of "database" file with all relevante info about people
    """
    input_file_names = extract_persons_and_identifiers(input_file_names)
    person_data = person_with_identifier(input_file_data)
    translated_people = []

    for person, identifier in input_file_names:
        result = [person, identifier]
        result.append(person_data[identifier]["it_IT"])
        result.append(person_data[identifier]["nl_NL"])
        result.append(person_data[identifier]["en_GB"])
        result.append(f"Comments: {person_data[identifier]['comments']}")
        result.append(f"Sources: {person_data[identifier]['sources']}")
        translated_people.append(result)

    list_of_translated_data(translated_people, "NameList")


def create_name_docx_with_style(input_file_names, input_file_data):
    """Creates a document with all names encountered in the input_file with translations
    in Italian, Dutch and English with added style (italic etc.)

    Args:
        input_file_names: Name of file with all people + their identifier
        input_file_data: Name of "database" file with all relevante info about people
    """
    input_file_names = extract_persons_and_identifiers(input_file_names)
    person_data = person_with_identifier(input_file_data)
    translated_people = []

    for person, identifier in input_file_names:
        result = [person, identifier]
        result.append(person_data[identifier]["it_IT"])
        result.append(person_data[identifier]["nl_NL"])
        result.append(person_data[identifier]["en_GB"])
        result.append(f"Comments: {person_data[identifier]['comments']}")
        result.append(f"Sources: {person_data[identifier]['sources']}")
        translated_people.append(result)

    list_of_translated_data_with_style(translated_people, "NameList")


if __name__ == "__main__":
    create_name_docx("inputs/NamesFondo+Identifier.docx", "inputs/Individuals.json")
    create_name_docx_with_style(
        "inputs/NamesFondo+Identifier.docx", "inputs/Individuals.json"
    )
