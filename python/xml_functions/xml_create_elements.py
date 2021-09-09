#!/usr/bin/env python3

from typing import Literal
from warnings import warn

from date_functions import extract_date
from lxml import etree

from xml_functions import add_unitdate


def basic_xml_file() -> tuple[
    etree._Element, etree._Element
]:  # pylint: disable=too-many-locals
    """Returns a basic .xml file based on EAD standard used for this project

    Returns:
        etree._Element: The root element of the .xml file
        etree._Element: The archdesc element of the .xml file
    """
    root = etree.Element("ead")

    # Eadheader
    eadheader = etree.SubElement(root, "eadheader")
    eaddid = etree.SubElement(eadheader, "eadid")
    comment = etree.Comment("Nationaal Archief")
    eaddid.append(comment)

    # Filedesc
    filedesc = etree.SubElement(eadheader, "filedesc")
    titlestmt = etree.SubElement(filedesc, "titlestmt")
    titleproper = etree.SubElement(titlestmt, "titleproper")
    titleproper.text = "Inventaris van het archieffonds van de Nederlandse Gezantschappen in Turijn en Rome, 1816 - 1874"  # pylint: disable=line-too-long
    author = titleproper = etree.SubElement(titlestmt, "author")
    author.text = "D.M. van Noord"
    publicationstmt = etree.SubElement(filedesc, "publicationstmt")
    publisher = etree.SubElement(publicationstmt, "publisher")
    publisher.text = "KNIR"
    date = etree.SubElement(
        publicationstmt, "date", calendar="gregorian", era="ce", normal="2021"
    )
    date.text = "(c) 2021"
    para = etree.SubElement(publicationstmt, "p", id="copyright")
    extref = etree.SubElement(
        para,
        "extref",
        linktype="simple",
        href="http://creativecommons.org/publicdomain/zero/1.0/",
        actuate="onrequest",
        show="new",
    )
    extref.text = "cc0"

    # Profiledesc
    profiledesc = etree.SubElement(eadheader, "profiledesc")
    # pylint: disable=trailing-whitespace
    language = """<langusage>This finding aid is written in 
            <language langcode="dut" scriptcode="Latn">Dutch</language>.
        </langusage>"""
    profiledesc.append(etree.fromstring(language))
    _ = etree.SubElement(profiledesc, "descrules")

    # Archdesc
    archdesc = etree.SubElement(root, "archdesc", level="fonds", type="inventory")
    archdescdid = etree.SubElement(archdesc, "did")
    _ = etree.SubElement(archdescdid, "unittitle")

    return root, archdesc


def volume_entry(
    parent_element: etree._Element,
    number: str,
    title: str,
    date: str,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> etree._Element:
    """Returns an .xml element for a volume at the c01 level

    Args:
        parent_element (etree._Element): The element to which the dossier element is appended
        number (str): The number of the volume
        title (str): Title of the dossier
        date (str): Date of the dossier
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation

    Returns:
        etree._Element: The dossier element at the c01 level
    """
    desc = etree.SubElement(parent_element, "dsc")
    head = etree.SubElement(desc, "head")
    head.text = f"{number} {title}"
    c01 = etree.SubElement(desc, "c01", level="series")
    c01_did = etree.SubElement(c01, "did")
    c01_did_id = etree.SubElement(c01_did, "unitid", type="series_code")
    c01_did_id.text = number + "."
    c01_did_title = etree.SubElement(c01_did, "unittitle")
    c01_did_title.text = title
    date1, date2 = extract_date(date, localization)
    add_unitdate(c01_did, date, date1, date2, "volume")
    return c01


def dossier_entry(  # pylint: disable=too-many-arguments
    parent_element: etree._Element,
    v_number: str,
    number: str,
    _: str,
    title: str,
    date: str,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> etree._Element:
    """Returns a dossier .xml element at the c02 level

    Args:
        parent_element (etree._Element): The element to which the dossier element is appended
        v_number (str): The volume number
        number (str): The dossier number
        pages (str): The pages of the dossier, unused now
        title (str): Title of the dossier
        date (str): Date of the dossier
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation

    Returns:
        etree._Element: The dossier element at the c02 level
    """
    c02 = etree.SubElement(parent_element, "c02", level="subseries")
    c02_head = etree.SubElement(c02, "head")
    c02_head.text = title
    c02_did = etree.SubElement(c02, "did")
    c02_did_id = etree.SubElement(c02_did, "unitid", type="series_code")
    c02_did_id.text = f"{v_number}.{number}"
    c02_did_title = etree.SubElement(c02_did, "unittitle")
    c02_did_title.text = title
    date1, date2 = extract_date(date, localization)
    add_unitdate(c02_did, date, date1, date2, "dossier")
    return c02


def file_entry(
    parent_element: etree._Element,
    pages: str,
    title: str,
    _: str,
    date: str,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> None:
    """Returns an .xml element for a file within a dossier

    Args:
        parent_element (etree._Element): The element to which the file element is appended
        pages (str): The pages of the files
        title (str): Title of the file
        place (str): The place of the file, no longer used
        date (str): Date of the file
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation
    """
    if parent_element.tag == "c01":
        c02 = etree.SubElement(parent_element, "c02", level="file")
        c02_did = etree.SubElement(c02, "did")
        c02_did_id = etree.SubElement(c02_did, "unitid", type="series_code")
        c02_did_id.text = f"pp. {pages}"
        c02_did_title = etree.SubElement(c02_did, "unittitle")
        c02_did_title.text = title
        date1, date2 = extract_date(date, localization)
        add_unitdate(c02_did, date, date1, date2, "file")
    elif parent_element.tag == "c02":
        c03 = etree.SubElement(parent_element, "c03", level="file")
        c03_did = etree.SubElement(c03, "did")
        c03_did_id = etree.SubElement(c03_did, "unitid", type="series_code")
        c03_did_id.text = f"pp. {pages}"
        c03_did_title = etree.SubElement(c03_did, "unittitle")
        c03_did_title.text = title
        date1, date2 = extract_date(date, localization)
        add_unitdate(c03_did, date, date1, date2, "file")
    else:
        warn("File was not handled correctly")
