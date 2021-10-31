#!/usr/bin/env python3
# type: ignore # pylint: disable-all

import json

from functions.data_find_names import create_person
from functions.json_translate import initialize_translation_database


def person_with_identifier(input_file: str) -> dict:
    """Creates a dictionary with all fully translated names and functions to be used in inventory

    Args:
        input_file: Name of the "database" file

    Raises:
        Exception: If the identifier is missing
        Exception: If the identifier is a duplicate

    Returns:
        dict: Dictionary with identifier as keys and translated full entries as values
    """
    with open(input_file, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    translation_data = initialize_translation_database()
    data_with_identifier = {}

    for identifier, data in persons.items():
        # Create data from persons
        full_name_function_nl_nl, _ = create_person("nl_NL", data, translation_data)
        full_name_function_it_it, _ = create_person("it_IT", data, translation_data)
        full_name_function_en_gb, _ = create_person("en_GB", data, translation_data)

        if identifier in data_with_identifier.keys():
            raise Exception(f"Identifier of {full_name_function_nl_nl} is a duplicate")

        data_with_identifier[identifier] = {
            "it_IT": full_name_function_it_it,
            "nl_NL": full_name_function_nl_nl,
            "en_GB": full_name_function_en_gb,
            "comments": data["comment"],
            "sources": "; ".join(data["sources"]),
        }

        print(full_name_function_nl_nl)

    return data_with_identifier


def used_functions_and_titles(input_file: str) -> tuple[list[str], list[str]]:
    """Creates two lists with all used functions and titles in Dutch

    Args:
        input_file: Name of the "database" file

    Returns:
        list: A list of all used functions
        list: A list of all used titles
    """
    with open(input_file, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    all_functions = []
    all_titles = []

    for _, data in persons.items():
        for i in data["functions"]:
            all_functions.append(i[0])
        for i in data["titles"]:
            all_titles.append(i)

        print(data["surname"])

    return sorted(list(set(all_functions))), sorted(list(set(all_titles)))


def used_names(input_file: str) -> list[str]:
    """Creates two lists with all names in Dutch

    Args:
        input_file: Name of the "database" file

    Returns:
        list: A list of all names
    """
    with open(input_file, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    translation_data = initialize_translation_database()
    all_full_names = []

    for _, data in persons.items():
        _, full_name_nl_nl = create_person("nl_NL", data, translation_data)
        all_full_names.append(full_name_nl_nl)

        print(full_name_nl_nl)

    return all_full_names
