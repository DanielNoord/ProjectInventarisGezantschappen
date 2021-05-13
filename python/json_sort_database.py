import json
import os


def sort_database(filename):
    """Sorts the entries in a database

    Args:
        filename (str): File name of initial database
    """
    with open(filename) as file:
        persons = json.load(file)
    del persons["$schema"]

    for identifier, data in persons.items():
        if len(data["sources"]) > 1 and data["sources"] != sorted(data["sources"]):
            persons[identifier]["sources"] = sorted(data["sources"])
            print(f"Sorted sources for {identifier}")
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
    with open("outputs/Individuals.json", "w", encoding="utf-8") as file:
        json.dump(persons, file, ensure_ascii=False, indent=4)
    print("Wrote file to outputs/Individuals.json")


if __name__ == "__main__":
    dname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dname)

    sort_database("inputs/Individuals.json")
