"""TODO: Outdated"""
import json

from functions.find_names import create_person
from functions.load_docx import extract_persons
from functions.translate import initialize_translation_database


def person_with_identifier(input_file):
    """Creates a dictionary with all fully translated names and functions to be used in inventory

    Args:
        input_file (str): Name of the "database" file

    Raises:
        Exception: If the identifier is missing
        Exception: If the identifier is a duplicate

    Returns:
        dict: Dictionary with identifier as keys and translated full entries as values
    """
    persons_in_file = extract_persons(input_file)
    translation_data = initialize_translation_database()
    data_with_identifier = {}

    for person in persons_in_file:
        if person[2] != "$":
            raise Exception(f"No identifier found for ${person}")

        # Create data from persons
        full_name_function_nl_nl, _, identifier, _, _, comments, sources = create_person(
            "nl_NL", person, translation_data
        )
        full_name_function_it_it, _, _, _, _, _, _ = create_person(
            "it_IT", person, translation_data
        )
        full_name_function_en_gb, _, _, _, _, _, _ = create_person(
            "en_GB", person, translation_data
        )

        if identifier in data_with_identifier.keys():
            raise Exception(f"Identifier of {full_name_function_nl_nl} is a duplicate")

        data_with_identifier[identifier] = {
            "it_IT": full_name_function_it_it,
            "nl_NL": full_name_function_nl_nl,
            "en_GB": full_name_function_en_gb,
            "comments": comments,
            "sources": sources
        }

        print(full_name_function_nl_nl)

    return data_with_identifier


def used_functions_and_titles(input_file):
    """Creates two lists with all used functions and titles in Dutch

    Args:
        input_file (str): Name of the "database" file

    Returns:
        list: A list of all used functions
        list: A list of all used titles
    """
    persons_in_file = extract_persons(input_file)
    translation_data = initialize_translation_database()
    all_functions = []
    all_titles = []

    for person in persons_in_file:
        _, full_name_nl_nl, _, functions, titles, _, _ = create_person(
            "nl_NL", person, translation_data
        )

        for i in functions:
            all_functions.append(i[0])
        for i in titles.split("| "):
            all_titles.append(i)

        print(full_name_nl_nl)

    return sorted(list(set(all_functions))), sorted(list(set(all_titles)))


def used_names(input_file):
    """Creates two lists with all names in Dutch

    Args:
        input_file (str): Name of the "database" file

    Returns:
        list: A list of all names
    """
    with open(filename) as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]
    translation_data = initialize_translation_database()
    all_full_names = []

    for person in persons_in_file:
        _, full_name_nl_nl, _, _, _, _, _ = create_person("nl_NL", person, translation_data)
        all_full_names.append(full_name_nl_nl)

        print(full_name_nl_nl)

    return all_full_names
