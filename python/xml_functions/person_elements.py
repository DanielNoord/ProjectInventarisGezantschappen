from typing import Literal

from lxml import etree
from typing_utils import Database


def add_persname(
    parent_element: etree._Element,
    identifier: str,
    database: Database,
    role: Literal["author", "receiver", "other"],
) -> None:
    """Add a persname to the parent element."""
    data = database.individuals[identifier]
    persname = etree.SubElement(
        parent_element, "persname", {"identifier": identifier, "relator": role}
    )
    etree.SubElement(persname, "part", {"localtype": "name"}).text = data["name"]
    etree.SubElement(persname, "part", {"localtype": "surname"}).text = data["surname"]

    etree.SubElement(persname, "part", {"localtype": "date_of_birth"}).text = data[
        "date_of_birth"
    ]
    etree.SubElement(
        persname, "part", {"localtype": "place_of_birth", "lang": "it"}
    ).text = data["place_of_birth"]
    birth_id = etree.SubElement(
        persname, "part", {"localtype": "place_of_birth_geonames_id"}
    )
    if data["place_of_birth"]:
        birth_id.text = str(database.placenames[data["place_of_birth"]]["geonames_id"])
    else:
        birth_id.text = ""

    etree.SubElement(persname, "part", {"localtype": "date_of_death"}).text = data[
        "date_of_death"
    ]
    etree.SubElement(
        persname, "part", {"localtype": "place_of_death", "lang": "it"}
    ).text = data["place_of_death"]
    death_id = etree.SubElement(
        persname, "part", {"localtype": "place_of_death_geonames_id"}
    )
    if data["place_of_death"]:
        death_id.text = str(database.placenames[data["place_of_death"]]["geonames_id"])
    else:
        death_id.text = ""
