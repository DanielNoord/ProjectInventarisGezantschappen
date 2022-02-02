from lxml import etree
from typing_utils import Database


def add_geognames(
    parent_element: etree._Element, place: str, database: Database, file_name: str
) -> None:
    """Adds a geogname to the parent element"""
    if place == "None":
        return

    data = database.placenames[place]
    geogname = etree.SubElement(
        parent_element,
        "geogname",
        {"identifier": f"http://www.geonames.org/{data['geonames_id']}"},
    )

    etree.SubElement(geogname, "part", {"lang": "it"}).text = place
    etree.SubElement(geogname, "part", {"lang": "en"}).text = data["en_GB"]
    etree.SubElement(geogname, "part", {"lang": "nl"}).text = data["nl_NL"]
    etree.SubElement(
        geogname, "geographiccoordinates", {"coordinatesystem": "WGS84"}
    ).text = f"{data['latitude']}, {data['longitude']}"
