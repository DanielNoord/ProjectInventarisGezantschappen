#!/usr/bin/env python3

import json

from database_searches import (
    convert_wikidata_to_isni,
    search_isni_api,
    search_wikidata,
    unspecified_wikidate,
)


def do_search_wikidata(filename: str) -> None:
    """Loads the database and starts searching wikidata."""
    with open(filename, encoding="utf-8") as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]

    search_wikidata(persons_in_file)


def get_unspecified_wikidata(filename: str) -> None:
    """Loads the database and prints entries with missing wikidata identifiers."""
    with open(filename, encoding="utf-8") as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]

    unspecified_wikidate(persons_in_file)


def check_isni(filename: str) -> None:
    """Loads the database and checks if wikidata id can be converted to ISNI dientifiers."""
    with open(filename, encoding="utf-8") as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]

    convert_wikidata_to_isni(persons_in_file)


def do_search_isni(filename: str) -> None:
    """Loads the database and starts searching ISNI."""
    with open(filename, encoding="utf-8") as file:
        persons_in_file = json.load(file)
    del persons_in_file["$schema"]

    search_isni_api(persons_in_file)


if __name__ == "__main__":
    # do_search_wikidata("inputs/Individuals.json")
    # get_unspecified_wikidata("inputs/Individuals.json")
    # check_isni("inputs/Individuals.json")
    do_search_isni("inputs/Individuals.json")
