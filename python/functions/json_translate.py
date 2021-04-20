import json


def initialize_translation_database():
    """Reads the files containing all translations of titles and functions

    Returns:
        list[dict, dict]: A list containing the dicts of title, functions and places translations
            For title and functions:
                Each entry (in "nl_NL") is a dictionary with the keys "nl_NL", "it_IT" and "en_GB"
                "nl_NL" is double but for ease of translation and reading the input-files in Word
            For places:
                Each entry (in "it_T") is a dictionary with the keys "nl_NL" and "en_GB"
    """
    with open("inputs/Translations/Titles.json") as file:
        titles = json.load(file)
    with open("inputs/Translations/TitlesUnsure.json") as file:
        titles = dict(titles, **json.load(file))
    with open("inputs/Translations/TitlesChanged.json") as file:
        titles = dict(titles, **json.load(file))
    del titles["$schema"]

    with open("inputs/Translations/Functions.json") as file:
        functions = json.load(file)
    with open("inputs/Translations/FunctionsUnsure.json") as file:
        functions = dict(functions, **json.load(file))
    with open("inputs/Translations/FunctionsChanged.json") as file:
        functions = dict(functions, **json.load(file))
    del functions["$schema"]

    with open("inputs/Translations/Placenames.json") as file:
        placenames = json.load(file)
    del placenames["$schema"]

    return [titles, functions, placenames]
