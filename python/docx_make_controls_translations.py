#!/usr/bin/env python3

import json

from docx_functions import list_of_translated_data


def create_controle_translations() -> None:
    """Create .docx files of all titles and functions found by the translate functions.

    Includes Italian and English translations on second and third row
    """
    with open("inputs/Translations/Titles.json", encoding="utf-8") as file:
        titles = json.load(file)
    del titles["$schema"]

    with open("inputs/Translations/Functions.json", encoding="utf-8") as file:
        functions = json.load(file)
    del functions["$schema"]

    with open("inputs/Translations/Placenames.json", encoding="utf-8") as file:
        placenames = json.load(file)
    del placenames["$schema"]

    with open("inputs/Translations/DocumentTitles.json", encoding="utf-8") as file:
        documents = json.load(file)
    del documents["$schema"]

    translated_titles = []
    translated_functions = []
    translated_places = []
    translated_documents = []

    for _, translations in sorted(titles.items()):
        result = [translations["nl_NL"]]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        result.append(f"position: {translations['position']}")
        translated_titles.append(result)

    for _, translations in sorted(functions.items()):
        result = [translations["nl_NL"]]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        translated_functions.append(result)

    for it_translation, translations in sorted(placenames.items()):
        result = [it_translation]
        result.append(translations["nl_NL"])
        result.append(translations["en_GB"])
        translated_places.append(result)

    for it_translation, translations in sorted(documents.items()):
        result = [it_translation]
        result.append(translations["nl_NL"])
        result.append(translations["en_GB"])
        translated_documents.append(result)

    list_of_translated_data(translated_titles, "Titles")
    list_of_translated_data(translated_functions, "Functions")
    list_of_translated_data(translated_places, "Placenames")
    list_of_translated_data(translated_documents, "DocumentTitles")


if __name__ == "__main__":
    create_controle_translations()
