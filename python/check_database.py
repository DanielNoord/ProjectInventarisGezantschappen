from functions.helper_functions.extract_date import extract_date
from functions.helper_functions.parse_function_string import function as read_function
from functions.helper_functions.parse_person_string import person as read_person
from functions.load_docx import extract_persons
from functions.translate import initialize_translation_database

def check_translations():
    """Checks the JSON files that contain all translations

    Raises:
        Exception: Whenever there are any duplicates or empty translations
    """
    translated_titles, translated_functions = initialize_translation_database()
    for key, translations in translated_titles.items():
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in titles at {key}")

    for key, translations in translated_functions.items():
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in functions at {key}")

    print("No missing translations found!")


def check_entries(input_file):
    """Checks whether the input file is correct and fits all criteria of a correct database file
    Checks for unknown functions, titles, etc.

    Args:
        input_file (str): Name of the input file

    Raises:
        Exception: Whenever something is missing/incorrect
    """
    translated_titles, translated_functions = initialize_translation_database()
    persons_in_file = extract_persons(input_file)
    identifiers = {}
    used_titles = []
    used_functions = []
    for person in persons_in_file:
        if person[2] != "$":
            raise Exception(f"No identifier found for ${person}")

        identifier, person_type, surname, _, _, titles, functions, _, _, _ = read_person(person)

        if identifier in identifiers.keys():
            raise Exception(f"Identifier of {surname} is a duplicate")

        if person_type == "":
            raise Exception(f"Type of {surname} is missing")

        if titles != "":
            titles = titles.split("| ")
            for title in titles:
                assert translated_titles[title]
                used_titles.append(title)

        if functions != "":
            functions = read_function(functions)
            for function, timeperiod in functions:
                assert translated_functions[function]
                if timeperiod is not None:
                    assert extract_date(timeperiod, "nl_NL")
                used_functions.append(function)
                
    unused_titles = [i for i in translated_titles.keys() if i not in used_titles]
    unused_functions = [
        i for i in translated_functions.keys() if i not in used_functions
    ]

    print(f"Found the following unused titles {unused_titles}")
    print(f"Found the following unused functions {unused_functions}")
    print("No missing translations found!")


if __name__ == "__main__":
    check_translations()
    check_entries("inputs/Eigennamen.docx")
    print("All checks passed!")
