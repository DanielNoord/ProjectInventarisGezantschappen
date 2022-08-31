from xml.etree import ElementTree

import requests
from typing_utils import IndividualsDictCleaned
from wikidataintegrator import wdi_core  # type: ignore[import]
from write_files import write_single_json_file


def convert_wikidata_to_isni(database: IndividualsDictCleaned) -> None:
    """Checks wikidata identifiers and sees if they can be converted to ISNI identifiers."""
    for data in database.values():
        if not data.get("ISNI:id", None) and data.get("wikidata:id", None):
            wikidata = wdi_core.WDItemEngine(
                wd_item_id=data["wikidata:id"]
            ).get_wd_json_representation()
            if isni_data := wikidata["claims"].get("P213", None):
                data["ISNI:id"] = isni_data[0]["mainsnak"]["datavalue"]["value"]
            else:
                data["ISNI:id"] = None

    database["$schema"] = "../static/JSON/Individuals.json"  # type: ignore[assignment]
    write_single_json_file(database, "outputs", "Individuals.json")


def search_isni_api(database: IndividualsDictCleaned) -> None:
    """Checks name and surname pairs and sees if they match with ISNI identifiers."""
    for data in database.values():
        if not data.get("ISNI:id", None):
            name = f"{data['name']} {data['surname']}".replace(" ", "+")
            response = requests.get(
                f"http://isni.oclc.org/sru/?query=pica.nw+%3D+%22{name}%22&operation=searchRetrieve&recordSchema=isni-b&maximumRecords=10",  # pylint: disable=line-too-long
                timeout=10,
            )

            records = list(
                ElementTree.fromstring(response.content).iter(
                    "{http://www.loc.gov/zing/srw/}record"
                )
            )

            if records:
                print("\n", data["name"], data["surname"])

            for record in records:
                uri = list(record.iter("isniURI"))[0].text
                try:
                    forename = list(record.iter("forename"))[0].text
                except IndexError:
                    forename = None
                try:
                    surname = list(record.iter("surname"))[0].text
                except IndexError:
                    surname = None
                print(forename, surname)
                print(uri)

    database["$schema"] = "../static/JSON/Individuals.json"  # type: ignore[assignment]
    write_single_json_file(database, "outputs", "Individuals.json")
