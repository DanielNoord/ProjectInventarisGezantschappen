#!/usr/bin/env python3

import json

from write_files import write_single_json_file


def sort_database(filename: str) -> None:
    """Sorts the entries in a database

    Args:
        filename: File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]

    for identifier, data in persons.items():
        if len(data["sources"]) > 1 and data["sources"] != sorted(data["sources"]):
            persons[identifier]["sources"] = sorted(data["sources"])
            print(f"Sorted sources for {identifier}")
        if len(data["sources_other"]) > 1 and data["sources_other"] != sorted(
            data["sources_other"]
        ):
            persons[identifier]["sources_other"] = sorted(data["sources_other"])
            print(f"Sorted sources_other for {identifier}")
        if len(data["titles"]) > 1 and data["titles"] != sorted(
            data["titles"], key=lambda x: (x[1] is not None, x[1])
        ):
            persons[identifier]["titles"] = sorted(
                data["titles"], key=lambda x: (x[1] is not None, x[1])
            )
            print(f"Sorted titles for {identifier}")
        if len(data["functions"]) > 1 and data["functions"] != sorted(
            data["functions"], key=lambda x: (x[1] is not None, x[1])
        ):
            persons[identifier]["functions"] = sorted(
                data["functions"], key=lambda x: (x[1] is not None, x[1])
            )
            print(f"Sorted functions for {identifier}")

    persons["$schema"] = "../static/JSON/Individuals.json"

    write_single_json_file(persons, "outputs", "Individuals.json")


if __name__ == "__main__":
    sort_database("inputs/Individuals.json")
