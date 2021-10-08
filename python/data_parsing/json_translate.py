import json
import re

from typing_utils import Database, TranslationDictCleaned, TranslationDictCleanedTitles


def initialize_translation_database() -> tuple[
    TranslationDictCleanedTitles, TranslationDictCleaned, TranslationDictCleaned
]:
    """Reads the files containing all translations of titles and functions"""
    with open("inputs/Translations/Titles.json", encoding="utf-8") as file:
        titles = json.load(file)
    del titles["$schema"]

    with open("inputs/Translations/Functions.json", encoding="utf-8") as file:
        functions = json.load(file)
    del functions["$schema"]

    with open("inputs/Translations/Placenames.json", encoding="utf-8") as file:
        placenames = json.load(file)
    del placenames["$schema"]

    return (titles, functions, placenames)


def initialize_database_for_xml() -> Database:
    """Reads the files containing all translations of titles and functions"""
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
        document_titles = json.load(file)
    del document_titles["$schema"]
    document_titles = {re.compile(k): v for k, v in document_titles.items()}

    with open("inputs/Individuals.json", encoding="utf-8") as file:
        individuals = json.load(file)
    del individuals["$schema"]

    return Database(document_titles, functions, placenames, titles, individuals)
