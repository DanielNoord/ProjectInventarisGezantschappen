import json

from functions.create_docx import list_of_translated_data


def create_controle_transaltions():
    """Create .docx files of all titles and functions found by the translate functions
    Includes Italian and English translations on second and third row
    """
    with open("inputs/Translations/Titles.json") as file1:
        titles = json.load(file1)
    del titles["$schema"]

    with open("inputs/Translations/Functions.json") as file2:
        functions = json.load(file2)
    del functions["$schema"]

    translated_titles = []
    translated_functions = []

    for _, translations in sorted(titles.items()):
        result = [translations["nl_NL"]]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        result.append(f"position: {translations['position']}")
        if translations.get("comment"):
            result.append(f"_Comment_: {translations['comment']}")
        translated_titles.append(result)

    for _, translations in sorted(functions.items()):
        result = [translations["nl_NL"]]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        if translations.get("comment"):
            result.append(f"_Comment_: {translations['comment']}")
        translated_functions.append(result)

    list_of_translated_data(translated_titles, "Titles")
    list_of_translated_data(translated_functions, "Functions")


if __name__ == "__main__":
    create_controle_transaltions()
