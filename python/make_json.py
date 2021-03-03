import json

from functions.helper_functions.parse_function_string import function as read_function
from functions.helper_functions.parse_person_string import person as read_person
from functions.load_docx import extract_persons


def create_json(input_file):
    data_with_identifier = {"$schema": "../static/JSON/Individuals.json"}
    persons_in_file = extract_persons(input_file)

    for person in persons_in_file:
        (
            identifier,
            surname,
            name,
            nationality,
            titles,
            functions,
            residence,
        ) = read_person(person)
        titles = titles.split("| ")
        functions = read_function(functions)
        data_with_identifier[identifier] = {
            "surname": surname,
            "name": name,
            "nationality": nationality,
            "titles": titles,
            "functions": functions,
            "place of residence": residence,
        }
    with open('outputs/Individuals.json', 'w', encoding='utf-8') as file:
        json.dump(data_with_identifier, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    create_json("inputs/Eigennamen.docx")
