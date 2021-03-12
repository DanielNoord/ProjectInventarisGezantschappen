import json
import re

import docx

from functions.create_docx import database
from functions.helper_functions.parse_function_string import function as read_function


def save_database(filename, previous_database=None):
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
    if previous_database:
        all_individuals = previous_database | all_individuals
    with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
        json.dump(all_individuals, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


def load_database(filename, skip_types):
    """Load database from .json and write .docx

    Args:
        filename (str): Name of the input file
        skip_types (list): Number of person types you might want to skip.
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    database(persons, "Individuals", skip_types)


def merge_database(filename, previous_database_filename):
    """Merges a file with a subset of the database (for example only a single person type)
    with a given previous database

    Args:
        filename (str): Name of file of new data
        previous_database_filename (str): Name of file of old data
    """
    with open(previous_database_filename) as file:
        prev_persons = json.load(file)
    save_database(filename, prev_persons)


if __name__ == "__main__":
    #save_database("inputs/Individuals.docx")
    load_database("inputs/Individuals.json", [0,1,2,4,5])
    #merge_database("inputs/Individuals_without_types_0,1,2,4,5.docx", "inputs/Individuals.json")
    pass
