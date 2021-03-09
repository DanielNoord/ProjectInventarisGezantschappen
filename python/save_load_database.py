import json
import re

import docx

from functions.create_docx import database
from functions.helper_functions.parse_function_string import function as read_function


def save_database(filename):
    """Load database from .docx and write .json

    Args:
        filename (str): Filename of the input file
    """
    doc = docx.Document(filename)
    all_individuals = {"$schema": "../static/JSON/Individuals.json"}

    for para in doc.paragraphs:
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
        ) = re.split(r"\n.*?: ", para.text)

        person_type = int(person_type)
        titles = titles.split("| ")
        functions = read_function(functions)
        sources = sources.replace("\n", "").split("| ")
        all_individuals[identifier] = {
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
        json.dump(all_individuals, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


def load_database(filename, skip_types=None):
    """Load database from .json and write .docx

    Args:
        filename (str): Name of the input file
        skip_types (list, optional): Number of person types you might want to skip.
            Defaults to None.
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    database(persons, "Individuals", skip_types)


if __name__ == "__main__":
    save_database("inputs/Individuals.docx")
    load_database("inputs/Individuals.json")
