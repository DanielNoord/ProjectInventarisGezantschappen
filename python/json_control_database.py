import json

from functions.helper_functions.extract_date import extract_date
from functions.json_translate import initialize_translation_database
from json_check_comments import check_all_comments
from json_check_placenames import check_all_placenames
from json_check_sources import check_all_sources


def check_translations():
    """Checks the JSON files that contain all translations

    Raises:
        Exception: Whenever there are any duplicates or empty translations
    """
    translated_titles, translated_functions, _ = initialize_translation_database()
    for key, translations in translated_titles.items():
        if key != translations["nl_NL"]:
            raise Exception(f"Found difference in Dutch translation and key for title {key}")
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in titles at {key}")

    for key, translations in translated_functions.items():
        if key != translations["nl_NL"]:
            raise Exception(f"Found difference in Dutch translation and key for function {key}")
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in functions at {key}")

    print("Finished checking translations: no missing or broken ones found!\n")


def check_entries(input_file):
    """Checks whether the input file is correct and fits all criteria of a correct database file
    Checks for unknown functions, titles, etc.

    Args:
        input_file (str): Name of the input file

    Raises:
        Exception: Whenever something is missing/incorrect
    """
    translated_titles, translated_functions, _ = initialize_translation_database()
    with open(input_file) as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]
    identifiers = {}
    used_titles = []
    used_functions = []

    for identifier, data in persons_in_file.items():
        if identifier[0] != "$":
            raise Exception(f"Incorrect identifier found for ${identifier}")

        if identifier in identifiers.keys():
            raise Exception(f"Identifier of {data['surname']} is a duplicate")

        if data["person_type"] not in [0, 1, 2, 3, 4, 5]:
            raise Exception(f"Type of {data['surname']} is invalid")

        if data["titles"] != [""]:
            for title, timeperiod in data["titles"]:
                assert translated_titles[title]
                if timeperiod is not None:
                    assert extract_date(timeperiod, "nl_NL")
                used_titles.append(title)

        if data["functions"] != [""]:
            for function, timeperiod in data["functions"]:
                assert translated_functions[function]
                if timeperiod is not None:
                    assert extract_date(timeperiod, "nl_NL")
                used_functions.append(function)

        if data["date_of_birth"] != [""]:
            assert extract_date(data["date_of_birth"], "nl_NL")

        if data["date_of_death"] != [""]:
            assert extract_date(data["date_of_birth"], "nl_NL")

    unused_titles = [i for i in translated_titles.keys() if i not in used_titles]
    unused_functions = [i for i in translated_functions.keys() if i not in used_functions]

    if unused_titles:
        print(f"    Found the following unused titles {unused_titles}")
    if unused_functions:
        print(f"    Found the following unused functions {unused_functions}")
    print(f"Finished checking database in {input_file}!\n")


if __name__ == "__main__":
    check_translations()
    check_entries("inputs/Individuals.json")
    check_all_sources("inputs/Individuals.json")
    check_all_comments("inputs/Individuals.json")
    check_all_placenames("inputs/Individuals.json")

    print("\nAll checks done!")
