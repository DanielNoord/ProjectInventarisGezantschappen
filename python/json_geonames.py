#!/usr/bin/env python3

import json
import os
from typing import Dict

import geocoder  # type: ignore


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
        placenames: Dict[str, Dict[str, str]] = json.load(file)
    del placenames["$schema"]

    # Load data
    for value in placenames.values():
        print(f"Looking for data for {value['en_GB']}")
        geoname = geocoder.geonames(value["en_GB"], key="danielnoord")
        geoname_detials = geocoder.geonames(
            geoname.geonames_id, key="danielnoord", method="details"
        )
        value["geonames:id"] = geoname.geonames_id
        value["geonames:wikipedia"] = geoname_detials.wikipedia

    # Re-add schema
    placenames["$schema"] = "../static/JSON/Placenames.json"  # type: ignore

    # Save file
    os.makedirs(
        os.path.join(os.getcwd(), "outputs/Translations"),
        exist_ok=True,
    )
    with open(
        filename.replace("inputs", "outputs"),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(placenames, file, ensure_ascii=False, indent=4)
    print(f"File written to {filename.replace('inputs', 'outputs')}")


if __name__ == "__main__":
    load_geonames("inputs/Translations/PlaceNames.json")
