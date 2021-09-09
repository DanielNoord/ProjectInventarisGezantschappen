#!/usr/bin/env python3

import json
import os

from data_parsing import initialize_translation_database


def transform_translations(dir_name: str, filename: str) -> None:
    """Load translations with the form Dutch {Dutch, Italian, English} and
    create file with Italian {Dutch, English} form for each key

    Args:
        dir_name (str): Name of the directory of file
        filename (str): Filename of the input file
    """
    new_data = {}
    with open("/".join((dir_name, filename)), "r", encoding="utf-8") as file:
        data = json.load(file)
    for entry, values in data.items():
        if entry != "$schema":
            entry = values["it_IT"]
            values.pop("it_IT")
        new_data[entry] = values

    os.makedirs(
        os.path.join(os.getcwd(), dir_name.replace("inputs", "outputs")),
        exist_ok=True,
    )
    with open(
        "/".join((dir_name.replace("inputs", "outputs"), filename)),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(new_data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"Wrote file to {'/'.join((dir_name.replace('inputs', 'outputs'), filename))}")


def translate_database(dir_name: str, filename: str) -> None:
    """Load database and translate all fields to their Italian form

    Args:
        dir_name (str): Name of the directory of file
        filename (str): Filename of the input file
    """
    translated_titles, translated_functions, _ = initialize_translation_database()

    new_data = {}
    with open("/".join((dir_name, filename)), "r", encoding="utf-8") as file:
        data = json.load(file)
    for entry, values in data.items():
        if entry != "$schema":
            if values["functions"]:
                for key, item in enumerate(values["functions"]):
                    values["functions"][key][0] = translated_functions[item[0]]["it_IT"]
            if values["titles"]:
                for key, item in enumerate(values["titles"]):
                    values["titles"][key][0] = translated_titles[item[0]]["it_IT"]
        new_data[entry] = values

    with open(
        "/".join((dir_name.replace("inputs", "outputs"), filename)),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(new_data, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"Wrote file to {'/'.join((dir_name.replace('inputs', 'outputs'), filename))}")


if __name__ == "__main__":
    transform_translations("inputs/Translations", "Functions.json")
    transform_translations("inputs/Translations", "Titles.json")
    translate_database("inputs", "Individuals.json")
