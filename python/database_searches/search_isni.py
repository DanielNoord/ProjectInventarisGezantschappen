from typing_utils import IndividualsDictCleaned
from wikidataintegrator import wdi_core  # type: ignore
from write_files import write_single_json_file


def convert_wikidata_to_isni(database: IndividualsDictCleaned) -> None:
    """Checks wikidata identifiers and sees if they can be converted to ISNI identifiers"""
    for data in database.values():
        if not data.get("ISNI:id", None) and data.get("wikidata:id", None):
            wikidata = wdi_core.WDItemEngine(
                wd_item_id=data["wikidata:id"]
            ).get_wd_json_representation()
            isni_data = wikidata["claims"].get("P213", None)
            if isni_data:
                data["ISNI:id"] = isni_data[0]["mainsnak"]["datavalue"]["value"]
            else:
                data["ISNI:id"] = None

    database["$schema"] = "../static/JSON/Individuals.json"  # type: ignore
    write_single_json_file(database, "outputs", "Individuals.json")
