import json


def create_statistics(filename, skip_types):
    """Print out statistics from from .json file

    Args:
        filename (str): Name of the input file
        skip_types (list): Number of person types you might want to skip.
    """
    c_comment = 0
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
        if data["person_type"] not in skip_types:
            if data["comment"] != "":
                c_comment += 1
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
    print(f"For the entries excluding the types {' and '.join(str(i) for i in skip_types)}")
    print(f"    Number of entries with comments: {c_comment}")
    print(f"    Number of entries with birth dates: {c_date_of_birth}")
    print(f"    Number of entries with death dates: {c_date_of_death}")
    print(f"    Number of entries with functions: {c_functions}")
    print(f"    Number of entries with images: {c_images}")
    print(f"    Number of entries with name: {c_name}")
    print(f"    Number of entries with place of birth: {c_place_of_birth}")
    print(f"    Number of entries with place of death: {c_place_of_death}")
    print(f"    Number of entries with sources: {c_sources}")
    print(f"    Number of entries with surname: {c_surname}")
    print(f"    Number of entries with titles: {c_titles}")


if __name__ == "__main__":
    create_statistics("inputs/Individuals.json", [])
