#!/usr/bin/env python3

import json

from typing_utils import Database, TranslationDictCleaned, TranslationDictCleanedTitles


def initialize_translation_database() -> tuple[
    TranslationDictCleanedTitles, TranslationDictCleaned, TranslationDictCleaned
]:
    """Reads the files containing all translations of titles and functions

    Returns:
        tuple[dict, dict, dict]: A list with the dicts of title, functions and places translations

            For title and functions:
                Each entry (in "nl_NL") is a dictionary with the keys "nl_NL", "it_IT" and "en_GB"
                "nl_NL" is double but for ease of translation and reading the input-files in Word
            For places:
                Each entry (in "it_T") is a dictionary with the keys "nl_NL" and "en_GB"
    """
    # TODO: Update docstring after transforming the databases
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

    with open("inputs/Individuals.json", encoding="utf-8") as file:
        individuals = json.load(file)
    del individuals["$schema"]

    return Database(document_titles, functions, placenames, titles, individuals)
