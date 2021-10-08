#!/usr/bin/env python3

import json
from typing import cast

import geocoder  # type: ignore

from typing_utils.translations_classes import TranslationDictCleanedPlacenames
from write_files import write_single_json_file


def load_geonames(filename: str) -> None:
    """Load geonames data for keys in json file

    Args:
        filename (str): Filename to load
    """

    # Load file
    with open(
        filename,
        encoding="utf-8",
    ) as file:
        placenames = json.load(file)
    del placenames["$schema"]
    placenames = cast(TranslationDictCleanedPlacenames, placenames)

    # Load data
    for value in placenames.values():
        print(f"Looking for data for {value['en_GB']}")
        geoname = geocoder.geonames(value["en_GB"], key="danielnoord")
        geoname_details = geocoder.geonames(
            geoname.geonames_id, key="danielnoord", method="details"
        )
        value["geonames_id"] = geoname.geonames_id
        if geoname_details.wikipedia:
            value["geonames_wikipedia"] = f"https://{geoname_details.wikipedia}"
        else:
            value["geonames_wikipedia"] = None

    # Re-add schema
    placenames["$schema"] = "../static/JSON/Placenames.json"

    write_single_json_file(placenames, "outputs/Translations", "Placenames.json")


def update_placenames_with_geonames(filename: str) -> None:
    """Pull data from geonames and populate our database with it"""
    # Load file
    with open(
        filename,
        encoding="utf-8",
    ) as file:
        placenames = json.load(file)
    del placenames["$schema"]
    placenames = cast(TranslationDictCleanedPlacenames, placenames)

    # Load data
    for value in placenames.values():
        if value["geonames_id"] is None:
            raise ValueError(f"{value['en_GB']} doesn't have a Geonames ID")
        geoname = geocoder.geonames(
            value["geonames_id"], method="details", key="danielnoord"
        )
        if geoname.feature_class not in {"P", "T", "H"}:  # Places, islands or seas
            raise ValueError(
                f"""Geonames ID for {value['en_GB']} is not a place, island or sea.
                Please check https://www.geonames.org/{value['geonames_id']}"""
            )

        # Populate fields
        value["latitude"] = geoname.lat
        value["longitude"] = geoname.lng
        if geoname.wikipedia:
            value["geonames_wikipedia"] = f"https://{geoname.wikipedia}"
        else:
            value["geonames_wikipedia"] = None

    # Re-add schema
    placenames["$schema"] = "../../static/JSON/Placenames.json"

    write_single_json_file(placenames, "outputs", "Placenames.json")


if __name__ == "__main__":
    # load_geonames("inputs/Translations/PlaceNames.json")
    update_placenames_with_geonames("inputs/Translations/PlaceNames.json")
