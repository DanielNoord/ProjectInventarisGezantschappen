import json


def create_statistics(filename, skip_types):
    """Print out statistics from from .json file

    Args:
        filename (str): Name of the input file
        skip_types (list): Number of person types you might want to skip.
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
        if data["person_type"] not in skip_types:
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
    print(f"For the entries excluding the types {' and '.join(str(i) for i in skip_types)}")
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


if __name__ == "__main__":
    create_statistics("inputs/Individuals.json", [])
