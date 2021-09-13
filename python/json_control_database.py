#!/usr/bin/env python3

import json

from data_parsing import initialize_translation_database
from date_functions import extract_date
from json_check_comments import check_all_comments
from json_check_placenames import check_all_placenames
from json_check_sources import check_all_sources
from typing_utils import (
    IndividualsDictEntry,
    TranslationDictCleaned,
    TranslationDictCleanedTitles,
)


def check_translations() -> None:
    """Checks the JSON files that contain all translations

    Raises:
        Exception: Whenever there are any duplicates or empty translations
    """
    translated_titles, translated_functions, _ = initialize_translation_database()
    for key, translations_titles in translated_titles.items():
        for translation in translations_titles.values():
            if translation == "":
                raise Exception(f"Found an empty translation in titles at {key}")

    for key, translations in translated_functions.items():
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in functions at {key}")

    print("Finished checking translations: no missing or broken ones found!\n")


def control_functions(
    data: IndividualsDictEntry,
    translated_functions: TranslationDictCleaned,
    identifier: str,
    used_functions: set[str],
) -> None:
    """Controls functions of the supplied data

    Args:
        data (dict): Data dict of identifier
        translated_functions (dict): Dict with titles currently translated
        identifier (str): Identifier of person with titles
        used_functions (set): List to track titles in use in database

    Raises:
        KeyError: When function is not found in current translations
        ValueError: When the function entry does not have 2 elements but too little
        ValueError: When the function entry does not have 2 elements but too many
        ValueError: When the timeperiod does not have a correct (1-12) month
        ValueError: Unrecognized ValueError's
    """
    try:
        for function, timeperiod in data["functions"]:
            try:
                assert translated_functions[function]
            except KeyError as err:
                raise KeyError(
                    f"Don't recgonize '{function}' from {identifier}. "
                    "Has it been added to inputs/Translations/Functions.json?"
                ) from err
            if timeperiod is not None:
                assert extract_date(timeperiod, "nl_NL")
            used_functions.add(function)
    except ValueError as err:
        if err.args[0] == "not enough values to unpack (expected 2, got 1)":
            raise ValueError(
                f"One of the functions of {identifier} does not follow standard pattern.\n"
                "Perhaps you need to split the date and function? Or is not empty correctly?"
            ) from err
        if err.args[0] == "too many values to unpack (expected 2)":
            raise ValueError(
                f"One of the functions of {identifier} does not follow standard pattern.\n"
                "There are too many strings"
            ) from err
        if err.args[0] == "month must be in 1..12":
            raise ValueError(
                f"{timeperiod} of '{function}' of {identifier} does not follow standard pattern.\n"
                "The month is not between 1 or 12 or you're not using a '/' correctly"
            ) from err
        print(err.args[0])
        if err.args[0].startswith("The first date"):
            raise ValueError(f"{err.args[0]} for '{function}' of {identifier}") from err
        raise ValueError(
            f"Unrecognized error. Please check the functions of {identifier} again"
        ) from err


def control_titles(
    data: IndividualsDictEntry,
    translated_titles: TranslationDictCleanedTitles,
    identifier: str,
    used_titles: set[str],
) -> None:
    """Controls titles of the supplied data

    Args:
        data (dict): Data dict of identifier
        translated_titles (dict): Dict with titles currently translated
        identifier (str): Identifier of person with titles
        used_titles (set): List to track titles in use in database

    Raises:
        KeyError: When title is not found in current translations
        ValueError: When the title entry does not have 2 elements but too little
        ValueError: When the title entry does not have 2 elements but too many
        ValueError: When the timeperiod does not have a correct (1-12) month
        ValueError: Unrecognized ValueError's
    """
    try:
        for title, timeperiod in data["titles"]:
            try:
                assert translated_titles[title]
            except KeyError as err:
                raise KeyError(
                    f"Don't recgonize '{title}' from {identifier}. "
                    "Has it been added to inputs/Translations/Titles.json?"
                ) from err
            if timeperiod is not None:
                assert extract_date(timeperiod, "nl_NL")
            used_titles.add(title)
    except ValueError as err:
        if err.args[0] == "not enough values to unpack (expected 2, got 1)":
            raise ValueError(
                f"One of the titles of {identifier} does not follow standard pattern.\n"
                "Perhaps you need to split the date and title? Or is not empty correctly?"
            ) from err
        if err.args[0] == "too many values to unpack (expected 2)":
            raise ValueError(
                f"One of the titles of {identifier} does not follow standard pattern.\n"
                "There are too many strings"
            ) from err
        if err.args[0] == "month must be in 1..12":
            raise ValueError(
                f"{timeperiod} of '{title}' of {identifier} does not follow standard pattern.\n"
                "The month is not between 1 or 12 or you're not using a '/' correctly"
            ) from err
        if err.args[0].startswith("The first date"):
            raise ValueError(f"{err.args[0]} for '{title}' of {identifier}") from err
        print(err.args[0])
        raise ValueError(
            f"Unrecognized error. Please check the titles of {identifier} again"
        ) from err


def control_date(timeperiod: str) -> None:
    """Controls date be calling extract_date() which raises exceptions for certain errors

    Args:
        timeperiod (str): String representation in standard date form
    """
    assert extract_date(timeperiod, "nl_NL")


def check_entries(input_file: str) -> None:  # pylint: disable=too-many-branches
    """Checks whether the input file is correct and fits all criteria of a correct database file
    Checks for unknown functions, titles, etc.

    Args:
        input_file (str): Name of the input file

    Raises:
        Exception: Whenever something is missing/incorrect
    """
    translated_titles, translated_functions, _ = initialize_translation_database()
    with open(input_file, encoding="utf-8") as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]
    identifiers = set()
    used_titles: set[str] = set()
    used_functions: set[str] = set()

    for identifier, data in persons_in_file.items():
        # Check if entry is correctly sorted
        if len(data["sources"]) > 1 and data["sources"] != sorted(data["sources"]):
            raise Exception(
                f"Incorrect sorting of sources found for {identifier}.\n"
                "Try running json_sort_database.py and copying "
                "outputs/Individuals.json to inputs/Individual.json"
            )

        if len(data["titles"]) > 1 and data["titles"] != sorted(
            data["titles"], key=lambda x: (x[1] is not None, x[1])
        ):
            raise Exception(
                f"Incorrect sorting of titles found for {identifier}.\n"
                "Make sure they are sorted based on their time"
            )

        if len(data["functions"]) > 1 and data["functions"] != sorted(
            data["functions"], key=lambda x: (x[1] is not None, x[1])
        ):
            raise Exception(
                f"Incorrect sorting of functions found for {identifier}.\n"
                "Make sure they are sorted based on their time"
            )

        if identifier[0] != "$":
            raise Exception(
                f"Incorrect identifier found for {identifier}.\n"
                "Identifiers should start with an '$'"
            )

        if identifier in identifiers:
            raise Exception(f"Identifier of {data['surname']} is a duplicate")
        identifiers.add(identifier)

        if data["person_type"] not in [0, 1, 2, 3, 4, 5, 6]:
            raise Exception(
                f"Type '{data['person_type']}' of {data['surname']} is invalid"
            )

        if data["titles"] != [""]:
            control_titles(data, translated_titles, identifier, used_titles)

        if data["functions"] != [""]:
            control_functions(data, translated_functions, identifier, used_functions)

        if data["date_of_birth"] != [""]:
            control_date(data["date_of_birth"])

        if data["date_of_death"] != [""]:
            control_date(data["date_of_death"])

    unused_titles = [i for i in translated_titles.keys() if i not in used_titles]
    unused_functions = [
        i for i in translated_functions.keys() if i not in used_functions
    ]

    if unused_titles:
        print(f"    Found the following unused titles {unused_titles}")
        print("    Please remove if no longer necessary!")
    if unused_functions:
        print(f"    Found the following unused functions {unused_functions}")
        print("    Please remove if no longer necessary!")
    print(f"Finished checking database in {input_file}!\n")


if __name__ == "__main__":
    check_translations()
    check_entries("inputs/Individuals.json")
    check_all_sources("inputs/Individuals.json")
    check_all_comments("inputs/Individuals.json")
    check_all_placenames("inputs/Individuals.json")

    print("All checks done!")
