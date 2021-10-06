from lxml import etree
from typing_utils.translations_classes import Translations


def add_geognames(
    parent_element: etree._Element, place: str, translations: Translations
) -> None:
    """Adds a geogname to the parent element"""
    if place == "None":
        return

    try:
        data = translations.placenames[place]
        geogname = etree.SubElement(
            parent_element,
            "geogname",
            {"identifier": f"http://www.geonames.org/{data['geonames_id']}"},
        )

        etree.SubElement(geogname, "part", {"lang": "it"}).text = place
        etree.SubElement(geogname, "part", {"lang": "en"}).text = data["en_GB"]
        etree.SubElement(geogname, "part", {"lang": "nl"}).text = data["nl_NL"]
    except KeyError:
        print(place)
    # TODO: Add geographiccoordinates element
