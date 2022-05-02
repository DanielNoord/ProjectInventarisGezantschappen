import json

import requests


def fetch_rkd_images(filename: str) -> None:
    """Checks all names in a database for hits in the RKD image database.

    Args:
        filename: File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        if not any(
            i for i in data["images"] if i.startswith("https://rkd.nl/explore/images")
        ):
            name = "+".join(
                [data["name"].replace(" ", "+"), data["surname"].replace(" ", "+")]
            )
            response = requests.get(
                f"https://rkd.nl/api/search/images?fieldset=brief&rows=50&query={name}"
            )
            if response.json()["response"]["docs"]:
                print(name)
            for image in response.json()["response"]["docs"]:
                print("", image["titel_engels"])
                print("", f"https://rkd.nl/explore/images/{image['priref']}")

    print("Finished checking for images!")


def fetch_rkd_artists(filename: str) -> None:
    """Checks all names in a database for hits in the RKD artists database.

    Args:
        filename: File name of initial database
    """
    with open(filename, encoding="utf-8") as file:
        persons = json.load(file)
    del persons["$schema"]
    for data in persons.values():
        if not any(
            i
            for i in data["sources"]
            if i.startswith("Dutch Institute for Art History")
        ):
            name = "+".join(
                [data["name"].replace(" ", "+"), data["surname"].replace(" ", "+")]
            )
            response = requests.get(
                f"https://rkd.nl//api/search/artists?fieldset=brief&rows=50&query={name}"
            )
            if response.json()["response"]["docs"]:
                print(name)
            for artist in response.json()["response"]["docs"]:
                print("", artist["kunstenaarsnaam"])
                print("", f"https://rkd.nl/explore/artists/{artist['priref']}")

    print("Finished checking for images!")


if __name__ == "__main__":
    fetch_rkd_images("inputs/Individuals.json")
    # fetch_rkd_artists("inputs/Individuals.json")
