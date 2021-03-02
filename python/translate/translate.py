import json

def initliaze_translation_database():
    """Reads the files containing all translations of titles and functions

    Returns:
        list[dict, dict]: A list containing the dictionaries of title and functions translations
            Each entry (in "nl_NL") is a dictionary with the keys "nl_NL", "it_IT" and "en_GB"
            "nl_NL" is double but for ease of translation and reading the input-files in Word
    """
    with open("inputs/Translations/Titles.json") as file1:
        titles = json.load(file1)

    with open("inputs/Translations/Functions.json") as file2:
        functions = json.load(file2)
    return [titles, functions]
