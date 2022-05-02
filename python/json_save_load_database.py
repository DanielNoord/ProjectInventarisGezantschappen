#!/usr/bin/env python3

import json
import re
from typing import Optional

import docx  # type: ignore[import]

from docx_functions import database, parse_function, parse_title
from typing_utils import IndividualsDict
from write_files import write_single_json_file


def save_database(  # pylint: disable=too-many-locals
    filename: str, previous_database: Optional[IndividualsDict] = None
) -> None:
    """Load database from .docx and write .json.

    Args:
        filename: Filename of the input file
        previous_database: Dict with data from previous database
    """
    doc = docx.Document(filename)
    all_individuals: IndividualsDict = {}

    # TODO: This does not work currently and removes fields we are using
    for para in doc.paragraphs:
        (
            identifier,
            person_type,
            surname,
            name,
            date_of_birth,
            place_of_birth,
            date_of_death,
            place_of_death,
            titles,
            functions,
            comment,
            comment_daniel,
            sources,
            images,
        ) = re.split(r"\n.*?: ", para.text)

        person_type = int(person_type)
        titles = parse_title(titles)
        functions = parse_function(functions)
        sources = sources.replace("\n", "").split("| ")
        images = images.replace("\n", "").split("| ")
        all_individuals[identifier] = {  # type: ignore[assignment]
            "surname": surname,
            "person_type": person_type,
            "name": name,
            "date_of_birth": date_of_birth,
            "place_of_birth": place_of_birth,
            "date_of_death": date_of_death,
            "place_of_death": place_of_death,
            "titles": titles,
            "functions": functions,
            "comment": comment,
            "comment_daniel": comment_daniel,
            "sources": sources,
            "images": images,
        }
    if previous_database:
        all_individuals = previous_database | all_individuals

    # Sort and Schema, shouldn't sort a dict but oh well..
    all_individuals = dict(sorted(all_individuals.items(), key=lambda item: item[0]))
    all_individuals = {"$schema": "../static/JSON/Individuals.json"} | all_individuals

    write_single_json_file(all_individuals, "outputs", "Individuals.json")


def load_database(filename: str, skip_types: list[int]) -> None:
    """Load database from .json and write .docx.

    Args:
        filename: Name of the input file
        skip_types: Number of person types you might want to skip.
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    database(persons, "Individuals", skip_types)


def merge_database(filename: str, previous_database_filename: str) -> None:
    """Merges a file with a subset of the database (for example only a single person type)
    with a given previous database

    Args:
        filename: Name of file of new data
        previous_database_filename: Name of file of old data
    """
    with open(previous_database_filename, encoding="utf-8") as file:
        prev_persons = json.load(file)
    save_database(filename, prev_persons)


if __name__ == "__main__":
    save_database("inputs/Individuals.docx")
    # load_database("inputs/Individuals.json", [])
    # merge_database("outputs/Individuals_without_types_0,1.docx", "inputs/Individuals.json")
