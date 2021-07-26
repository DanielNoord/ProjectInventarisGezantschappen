#!/usr/bin/env python3

import json


def check_all_placenames(filename):
    """Checks all placenames in a given database are Italian and known

    Args:
        filename (str): File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    with open("inputs/Translations/Placenames.json", encoding="utf-8") as file:
        placenames = json.load(file)

    for identifier, data in persons.items():
        if data["place_of_birth"] != "" and data["place_of_birth"] not in placenames:
            print(f"Don't recognize place of birth of {identifier}: {data['place_of_birth']}")
        if data["place_of_death"] != "" and data["place_of_death"] not in placenames:
            print(f"Don't recognize place of death of {identifier}: {data['place_of_death']}")

    print(f"Finished checking placenames in {filename}\n")


if __name__ == "__main__":
    check_all_placenames("inputs/Individuals.json")
