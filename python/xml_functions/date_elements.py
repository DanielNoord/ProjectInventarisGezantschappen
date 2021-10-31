from lxml import etree
from typing_utils import DateData


def add_unitdate(
    parent_element: etree._Element, datestring: str, date: DateData
) -> None:
    """Creates and appends an unitdate element"""
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


def add_dateset(
    parent_element: etree._Element, datestring: str, date: DateData
) -> None:
    """Creates and appends an unitdate element"""
    dateset = etree.SubElement(parent_element, "dateset")

    # Add Italian unitdate
    datesing_element_it = etree.SubElement(
        dateset,
        "datesingle",
        {"standarddate": datestring, "lang": "it"},
    )
    if date.date1_it:
        if date.date2_it:
            datesing_element_it.text = f"{date.date1_it} al {date.date2_it}"
        else:
            datesing_element_it.text = f"{date.date1_it}"
    elif date.date2_it:
        datesing_element_it.text = f"Al {date.date2_it}"
        raise ValueError("This element only has an end date. Check if this is correct!")

    # Add English unitdate
    datesing_element_en = etree.SubElement(
        dateset,
        "datesingle",
        {"standarddate": datestring, "lang": "en"},
    )
    if date.date1_en:
        if date.date2_en:
            datesing_element_en.text = f"{date.date1_en} till {date.date2_en}"
        else:
            datesing_element_en.text = f"{date.date1_en}"
    elif date.date2_en:
        datesing_element_en.text = f"Till {date.date2_en}"

    # Add Dutch unitdate
    datesing_element_nl = etree.SubElement(
        dateset,
        "datesingle",
        {"standarddate": datestring, "lang": "nl"},
    )
    if date.date1_nl:
        if date.date2_nl:
            datesing_element_nl.text = f"{date.date1_nl} tot en met {date.date2_nl}"
        else:
            datesing_element_nl.text = f"{date.date1_nl}"
    elif date.date2_nl:
        datesing_element_nl.text = f"Tot en met {date.date2_nl}"
