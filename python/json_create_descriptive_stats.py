#!/usr/bin/env python3

import json
import os


def create_type_statistics(
    filename, type_list, skip
):  # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    """Print out statistics from from .json file for specified person types

    Args:
        filename (str): Name of the input file
        type_list (list): Number of person types you might want to skip.
        skip (bool): Whether type_list should be seen as a skip list or as a list to select
    """
    c_comment = 0
    c_comment_daniel = 0
    c_date_of_birth = 0
    c_date_of_death = 0
    c_functions = 0
    c_images = 0
    c_name = 0
    c_place_of_birth = 0
    c_place_of_death = 0
    c_sources = 0
    c_surname = 0
    c_titles = 0

    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        if (skip and data["person_type"] not in type_list) or (
            not skip and data["person_type"] in type_list
        ):
            if data["comment"] != "":
                c_comment += 1
            if data["comment_daniel"] != "":
                c_comment_daniel += 1
            if data["date_of_birth"] != "":
                c_date_of_birth += 1
            if data["date_of_death"] != "":
                c_date_of_death += 1
            if data["functions"] != []:
                c_functions += 1
            if data["images"] != [""]:
                c_images += 1
            if data["name"] != "":
                c_name += 1
            if data["place_of_birth"] != "":
                c_place_of_birth += 1
            if data["place_of_death"] != "":
                c_place_of_death += 1
            if data["sources"] != [""]:
                c_sources += 1
            if data["surname"] != "":
                c_surname += 1
            if data["titles"] != []:
                c_titles += 1
    start_string = "    Number of entries with"
    if type_list != [] and skip or type_list != [0, 1, 2, 3, 4, 5] and not skip:
        type_string = f"the types {' and '.join(str(i) for i in type_list)}:"
    else:
        type_string = "the full database:"

    if skip:
        print(f"For the entries excluding {type_string}")
    else:
        print(f"For the entries of {type_string}")
    print(f"{start_string} comments: {c_comment}, {c_comment/c_surname:.2%}")
    print(f"{start_string} 'Daniel' comment: {c_comment_daniel}, {c_comment_daniel/c_surname:.2%}")
    print(f"{start_string} birth dates: {c_date_of_birth}, {c_date_of_birth/c_surname:.2%}")
    print(f"{start_string} death dates: {c_date_of_death}, {c_date_of_death/c_surname:.2%}")
    print(f"{start_string} functions: {c_functions}, {c_functions/c_surname:.2%}")
    print(f"{start_string} images: {c_images}, {c_images/c_surname:.2%}")
    print(f"{start_string} name: {c_name}, {c_name/c_surname:.2%}")
    print(f"{start_string} place of birth: {c_place_of_birth}, {c_place_of_birth/c_surname:.2%}")
    print(f"{start_string} place of death: {c_place_of_death}, {c_place_of_death/c_surname:.2%}")
    print(f"{start_string} sources: {c_sources}, {c_sources/c_surname:.2%}")
    print(f"{start_string} surname: {c_surname}, {c_surname/c_surname:.2%}")
    print(f"{start_string} titles: {c_titles}, {c_titles/c_surname:.2%}")


def create_total_statistics(filename):
    """Print out statistics from from .json file for total file

    Args:
        filename (str): Name of the input file
    """
    c_types = [0, 0, 0, 0, 0, 0]

    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        c_types[data["person_type"]] += 1

    start_string = "    Number of entries with"
    total_count = len(persons.keys())
    print("For the full database:")
    print(f"{start_string} type 0: {c_types[0]}, {c_types[0]/total_count:.2%}")
    print(f"{start_string} type 1: {c_types[1]}, {c_types[1]/total_count:.2%}")
    print(f"{start_string} type 2: {c_types[2]}, {c_types[2]/total_count:.2%}")
    print(f"{start_string} type 3: {c_types[3]}, {c_types[3]/total_count:.2%}")
    print(f"{start_string} type 4: {c_types[4]}, {c_types[4]/total_count:.2%}")
    print(f"{start_string} type 5: {c_types[5]}, {c_types[5]/total_count:.2%}")


if __name__ == "__main__":
    dname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dname)

    create_type_statistics("inputs/Individuals.json", [0, 1, 2, 3, 4, 5], False)
    create_total_statistics("inputs/Individuals.json")
