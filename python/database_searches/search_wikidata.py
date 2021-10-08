from typing_utils import IndividualsDictCleaned
from wikidataintegrator import wdi_core  # type: ignore
from write_files import write_single_json_file


def search_wikidata(database: IndividualsDictCleaned) -> None:
    """Searches wikidata for 10 best matches"""
    for data in database.values():
        if not data.get("wikidata:id", None):
            ids = wdi_core.WDItemEngine.get_wd_search_results(
                f"{data['name']} {data['surname']}"
            )
            if ids:
                print(f"{data['name']} {data['surname']}:")
                if len(ids) > 10:
                    ids = ids[:10]
                for person_id in ids:
                    try:
                        print(
                            wdi_core.WDItemEngine(
                                wd_item_id=person_id
                            ).get_wd_json_representation()["labels"]["en"]["value"]
                        )
                    except KeyError:
                        try:
                            print(
                                wdi_core.WDItemEngine(
                                    wd_item_id=person_id
                                ).get_wd_json_representation()["labels"]["it"]["value"]
                            )
                        except KeyError:
                            try:
                                print(
                                    wdi_core.WDItemEngine(
                                        wd_item_id=person_id
                                    ).get_wd_json_representation()["labels"]["nl"][
                                        "value"
                                    ]
                                )
                            except KeyError:
                                print("Unrecognized language of entry")
                    print(f"https://www.wikidata.org/wiki/{person_id}")


def unspecified_wikidate(database: IndividualsDictCleaned) -> None:
    """Prints out entries without a wikidata identifier"""
    for entry, data in database.items():
        if not data.get("wikidata:id", None):
            print(f"{entry}: {data['name']} {data['surname']}")


def convert_wikidata_to_isni(database: IndividualsDictCleaned) -> None:
    """Checks wikidata identifiers and sees if they can be converted to ISNI identifiers"""
    for data in database.values():
        if data.get("wikidata:id", None):
            wikidata = wdi_core.WDItemEngine(
                wd_item_id=data["wikidata:id"]
            ).get_wd_json_representation()
            isni_data = wikidata["claims"].get("P213", None)
            if isni_data:
                data["ISNI:id"] = isni_data[0]["mainsnak"]["datavalue"]["value"]
            else:
                data["ISNI:id"] = None
        else:
            data["ISNI:id"] = None
    write_single_json_file(database, "outputs", "Individuals.json")
