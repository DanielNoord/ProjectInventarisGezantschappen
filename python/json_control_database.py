#!/usr/bin/env python3

import json
import re
from typing import cast

from data_parsing import initialize_translation_database
from database_controls import (
    check_all_placenames,
    check_all_sources,
    check_translations,
    control_date,
    control_functions,
    control_titles,
    is_isni,
)
from typing_utils.translations_classes import IndividualsDictCleaned


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
    persons_in_file = cast(IndividualsDictCleaned, persons_in_file)

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

        if len(data["sources_other"]) > 1 and data["sources_other"] != sorted(
            data["sources_other"]
        ):
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

        if isinstance(data["wikidata:id"], str):
            if not re.match(r"^Q\d+$", data["wikidata:id"]):
                raise ValueError(
                    "Wikidata ID is incorrect. If individual has no identifier use None"
                )

        if isinstance(["ISNI:id"], str):
            if not is_isni(data["ISNI:id"]):
                raise ValueError(
                    f"ISNI ID of {identifier} is incorrect. If person has no identifier use None"
                )

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
    check_all_placenames("inputs/Individuals.json")

    print("All checks done!")
