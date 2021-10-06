from lxml import etree
from typing_utils.translations_classes import Database


def add_persname(
    parent_element: etree._Element, identifier: str, database: Database
) -> None:
    """Adds a persname to the parent element"""
    data = database.individuals[identifier]
    persname = etree.SubElement(
        parent_element, "persname", {"identifier": identifier, "relator": "Unknown"}
    )
    etree.SubElement(persname, "part", {"localtype": "name"}).text = data["name"]
    etree.SubElement(persname, "part", {"localtype": "surname"}).text = data["surname"]
    etree.SubElement(persname, "part", {"localtype": "date_of_birth"}).text = data[
        "date_of_birth"
    ]
    etree.SubElement(persname, "part", {"localtype": "place_of_birth"}).text = data[
        "place_of_birth"
    ]
    etree.SubElement(persname, "part", {"localtype": "date_of_death"}).text = data[
        "date_of_death"
    ]
    etree.SubElement(persname, "part", {"localtype": "place_of_death"}).text = data[
        "place_of_death"
    ]
