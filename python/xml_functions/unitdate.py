#!/usr/bin/env python3

from lxml import etree
from typing_classes import DateData


def add_unitdate(  # pylint: ignore=too-many-branches
    parent_element: etree._Element, datestring: str, date: DateData
) -> None:
    """Creates and appends an unitdate element"""
    if not datestring:
        raise ValueError(f"No datestring provided for {parent_element}")

    # Add Italian unitdate
    udate_element_it = etree.SubElement(
        parent_element,
        "unitdate",
        {"calendar": "gregorian", "era": "ce", "normal": datestring, "lang": "it"},
    )
    if date.date1_it:
        if date.date2_it:
            udate_element_it.text = f"{date.date1_it} al {date.date2_it}"
        else:
            udate_element_it.text = f"{date.date1_it}"
    elif date.date2_it:
        udate_element_it.text = f"Al {date.date2_it}"
        raise ValueError("This element only has an end date. Check if this is correct!")

    # Add English unitdate
    udate_element_en = etree.SubElement(
        parent_element,
        "unitdate",
        {"calendar": "gregorian", "era": "ce", "normal": datestring, "lang": "en"},
    )
    if date.date1_en:
        if date.date2_en:
            udate_element_en.text = f"{date.date1_en} till {date.date2_en}"
        else:
            udate_element_en.text = f"{date.date1_en}"
    elif date.date2_en:
        udate_element_en.text = f"Till {date.date2_en}"

    # Add Dutch unitdate
    udate_element_nl = etree.SubElement(
        parent_element,
        "unitdate",
        {"calendar": "gregorian", "era": "ce", "normal": datestring, "lang": "nl"},
    )
    if date.date1_nl:
        if date.date2_nl:
            udate_element_nl.text = f"{date.date1_nl} tot en met {date.date2_nl}"
        else:
            udate_element_nl.text = f"{date.date1_nl}"
    elif date.date2_nl:
        udate_element_nl.text = f"Tot en met {date.date2_nl}"
