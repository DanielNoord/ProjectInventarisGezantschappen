from lxml import etree
from typing_utils import Database


def add_geognames(
    parent_element: etree._Element, place: str, database: Database
) -> None:
    """Adds a geogname to the parent element"""
    if place == "None":
        return

    # TODO: REMOVE THIS!!!!!
    try:
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
    except KeyError:
        with open("outputs/missing_placenames", "a", encoding="utf-8") as file:
            # pylint: disable-next=line-too-long
            c01 = parent_element.getparent().getparent().getparent().getparent().getparent()  # type: ignore
            volume = c01.getchildren()[0].getchildren()[0].text  # type: ignore
            print(f"|Vol: {volume}|{place}", file=file)
