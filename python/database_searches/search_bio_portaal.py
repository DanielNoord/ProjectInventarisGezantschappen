import json

import requests


def fetch_bio_portaal_names(filename: str) -> None:
    """Checks all names in a database for hits in the Biografisch Portaal database.

    Args:
        filename: File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        if not any(i for i in data["sources"] if i.count("Biografisch Portaal van Nederland")):
            name = "+".join([data["name"].replace(" ", "+"), data["surname"].replace(" ", "+")])
            response = requests.get(
                f"http://www.biografischportaal.nl/personen/json?search_name={name}",
                timeout=10,
            )
            if response.json() != []:
                print(name)
                if len(response.json()) > 99:
                    print("Too many results\n")
                for hit in response.json():
                    print("", hit["url_biografie"])
                    print("", hit["namen"])
                    print(
                        "",
                        "Birth:",
                        [i["when"] for i in hit["event"] if i["type"] == "birth"],
                    )
                    print(
                        "",
                        "Death:",
                        [i["when"] for i in hit["event"] if i["type"] == "death"],
                        "\n",
                    )

    print("Finished checking in Biografisch Portaal database!")


if __name__ == "__main__":
    fetch_bio_portaal_names("inputs/Individuals.json")
