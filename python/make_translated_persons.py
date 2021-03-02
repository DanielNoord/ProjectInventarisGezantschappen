from create_data import person_with_identifier
from functions.create_docx import list_of_translated_data
from functions.load_docx import extract_persons_and_identifiers


def create_name_docx(input_file_names, input_file_data):
    """Creates a document with all names encountered in the input_file with translations
    in Italian, Dutch and English

    Args:
        input_file_names (str): Name of file with all people + their identifier
        input_file_data (str): Name of "database" file with all relevante info about people
    """
    input_file_names = extract_persons_and_identifiers(input_file_names)
    person_data = person_with_identifier(input_file_data)
    translated_people = []

    for person, identifier in input_file_names:
        result = [person, identifier]
        result.append(person_data[identifier]["it_IT"])
        result.append(person_data[identifier]["nl_NL"])
        result.append(person_data[identifier]["en_GB"])
        translated_people.append(result)

    list_of_translated_data(translated_people, "NameList")


if __name__ == "__main__":
    create_name_docx("inputs/NamesFondo+Identifier.docx", "inputs/Eigennamen.docx")
