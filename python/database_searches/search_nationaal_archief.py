import json

import requests


def fetch_na_inventaris(filename: str) -> None:
    """Checks all names in a database for hits in the Nationaal Archief inventaris database.
    Only counts as hit when the name matches something in the document descriptions,
    inventory description matches are ignored

    Args:
        filename (str): File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        if not any(
            i for i in data["sources"] if i.startswith("Nationaal Archief, The Hague")
        ):
            name = (
                "+".join(
                    [data["name"].replace(" ", "+"), data["surname"].replace(" ", "+")]
                )
                .replace("{", "")
                .replace("}", "")
            )
            response = requests.get(
                f"https://service.archief.nl/hub3/api/ead/search?q={name}&rows=100"
            )
            if response.json()["archiveCount"] > 0:
                print(name)
                if response.json()["archiveCount"] > 100:
                    print("Too many hits")
                for hit in response.json()["archives"]:
                    if hit["cLevelCount"] > -1:
                        print("", hit["title"])
                        print(
                            "",
                            f"Nationaal Archief, The Hague, '{hit['title']}', inventory number: {hit['inventoryID']}",  # pylint: disable=line-too-long
                        )
                        print(
                            "",
                            f"https://www.nationaalarchief.nl/onderzoeken/archief/{hit['inventoryID']}?query={name}&search-type=inventory",  # pylint: disable=line-too-long
                        )

    print("Finished checking in National Archief inventaris database!")


if __name__ == "__main__":
    fetch_na_inventaris("inputs/Individuals.json")
