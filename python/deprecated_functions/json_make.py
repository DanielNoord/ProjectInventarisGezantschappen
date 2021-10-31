#!/usr/bin/env python3
# type: ignore # pylint: disable-all

import json

from functions.docx_load import extract_persons, extract_translations
from functions.helper_functions.parse_function_string import function as read_function
from functions.helper_functions.parse_person_string import person as read_person
from functions.helper_functions.parse_title_string import title as read_title


def create_json_database(input_file):
    """Creates JSON file from old Eigennamen file

    Args:
        input_file: File name of database file
    """
    data_with_identifier = {"$schema": "../static/JSON/Individuals.json"}
    persons_in_file = extract_persons(input_file)

    for person in persons_in_file:
        (
            identifier,
            person_type,
            surname,
            name,
            nationality,
            titles,
            functions,
            residence,
            comment,
            sources,
        ) = read_person(person)
        person_type = int(person_type)
        titles = read_title(titles)
        functions = read_function(functions)
        sources = sources.split("| ")
        data_with_identifier[identifier] = {
            "surname": surname,
            "person_type": person_type,
            "name": name,
            "nationality": nationality,
            "titles": titles,
            "functions": functions,
            "place of residence": residence,
            "comment": comment,
            "sources": sources,
        }
    with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
        json.dump(data_with_identifier, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


def create_json_translations(input_file, file_name):
    """Creates JSON from translation file

    Args:
        input_file: Name of input file
        file_name: Name of output file
    """
    translations = {"$schema": f"../static/JSON/{file_name}.json"}
    translations = dict(translations, **extract_translations(input_file))

    with open(f"outputs/{file_name}.json", "w", encoding="utf-8") as file:
        json.dump(translations, file, ensure_ascii=False, indent=4)
    print(f"Wrote file to outputs/{file_name}.json")


if __name__ == "__main__":
    # create_json_database("inputs/Eigennamen.docx")
    # create_json_translations("inputs/Translations/TranslatedFunctions.docx", "Functions")
    # create_json_translations("inputs/Translations/TranslatedTitles.docx", "Titles")
    pass
