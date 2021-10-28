import re
from typing import Optional

from date_functions import create_date_data
from lxml import etree
from typing_utils import Database, FileData, VolData

from xml_functions import (
    add_dateset,
    add_geognames,
    add_persname,
    add_unitdate,
    add_unittitle,
    add_dao
)


def basic_xml_file() -> tuple[etree._Element, etree._Element]:
    """Returns a basic .xml file based on EAD standard used for this project

    Returns:
        etree._Element: The root element of the .xml file
        etree._Element: The archdesc element of the .xml file
    """
    root = etree.Element("ead")

    # Control
    control = etree.SubElement(root, "control")
    eaddid = etree.SubElement(control, "recordid")
    comment = etree.Comment("TO BE DECIDED")
    eaddid.append(comment)

    # Filedesc
    filedesc = etree.SubElement(control, "filedesc")
    titlestmt = etree.SubElement(filedesc, "titlestmt")
    etree.SubElement(
        titlestmt, "titleproper", {"lang": "dut"}
    ).text = "Inventaris van het archieffonds van de Nederlandse Gezantschappen in Turijn en Rome, 1816 - 1874"  # pylint: disable=line-too-long
    etree.SubElement(
        titlestmt, "titleproper", {"lang": "en"}
    ).text = (
        "Inventory of the archief of the Dutch Legation in Turin and Rome, 1816 - 1874"
    )
    etree.SubElement(
        titlestmt, "titleproper", {"lang": "it"}
    ).text = "Inventario del fondo archivistico delle Legazioni Olandesi a Torino e Roma, 1816 - 1874"  # pylint: disable=line-too-long
    etree.SubElement(titlestmt, "author").text = "KNIR/ISTRIT"
    publicationstmt = etree.SubElement(filedesc, "publicationstmt")
    etree.SubElement(publicationstmt, "publisher").text = "KNIR/ISTRIT"
    etree.SubElement(
        publicationstmt, "date", calendar="gregorian", era="ce", normal="2021"
    ).text = "(c) 2021"

    # Required elements
    etree.SubElement(control, "maintenancestatus", {"value": "new"})
    maint_agency = etree.SubElement(control, "maintenanceagency")
    etree.SubElement(maint_agency, "agencyname").text = "KNIR"
    etree.SubElement(maint_agency, "agencyname").text = "ISTRIT"

    # Languagedeclaration
    languagedeclaration = etree.SubElement(control, "languagedeclaration")
    etree.SubElement(
        languagedeclaration, "language", {"langcode": "eng"}
    ).text = "English"
    etree.SubElement(
        languagedeclaration, "script", {"scriptcode": "Latin"}
    ).text = "Latin"

    # Maintenancehistory
    maintenancehistory = etree.SubElement(control, "maintenancehistory")
    maint_event = etree.SubElement(maintenancehistory, "maintenanceevent")
    etree.SubElement(maint_event, "eventtype", {"value": "created"})
    etree.SubElement(
        maint_event, "eventdatetime", {"standarddatetime": "2021"}
    ).text = "2021"
    etree.SubElement(maint_event, "agenttype", {"value": "human"})
    etree.SubElement(maint_event, "agent").text = "Daniël van Noord"
    etree.SubElement(maint_event, "eventdescription").text = "Finding aid created."

    # Archdesc
    archdesc = etree.SubElement(
        root, "archdesc", {"level": "fonds", "localtype": "inventory"}
    )
    archdesc_did = etree.SubElement(archdesc, "did")
    etree.SubElement(archdesc_did, "unittitle")
    archdesc_dsc = etree.SubElement(archdesc, "dsc", {"dsctype": "combined"})

    return root, archdesc_dsc


def volume_entry(
    archdesc_dsc: etree._Element, volume_data: VolData, database: Database
) -> tuple[etree._Element, Optional[re.Pattern[str]]]:
    """Returns an .xml element for a volume at the c01 level"""
    c01 = etree.SubElement(archdesc_dsc, "c01", level="series")
    c01_did = etree.SubElement(c01, "did")
    etree.SubElement(c01_did, "unitid").text = volume_data.num

    used_trans = add_unittitle(c01_did, volume_data.title, database, volume_data.date)

    date_data = create_date_data(volume_data.date)
    add_unitdate(c01_did, volume_data.date, date_data)

    return c01, used_trans


def dossier_entry(  # pylint: disable=too-many-arguments
    parent_element: etree._Element,
    v_number: str,
    number: str,
    title: str,
    date: str,
    database: Database,
) -> tuple[etree._Element, Optional[re.Pattern[str]]]:
    """Returns a dossier .xml element at the c02 level"""
    c02 = etree.SubElement(parent_element, "c02", level="subseries")
    c02_did = etree.SubElement(c02, "did")
    etree.SubElement(c02_did, "unitid").text = f"{v_number}.{number}"

    pattern = add_unittitle(c02_did, title, database, date)

    date_data = create_date_data(date)
    add_unitdate(c02_did, date, date_data)
    return c02, pattern


def file_entry(
    parent_element: etree._Element,
    file_data: FileData,
    database: Database,
) -> tuple[etree._Element, Optional[re.Pattern[str]]]:
    """Creates an .xml element for a file within a dossier/volume"""

    if parent_element.tag == "c01":
        file_element = etree.SubElement(parent_element, "c02", level="file")
    elif parent_element.tag == "c02":
        file_element = etree.SubElement(parent_element, "c03", level="file")
    else:
        raise ValueError(f"File was not handled correctly{file_data.title}")
    file_did = etree.SubElement(file_element, "did")

    # ID
    etree.SubElement(file_did, "unitid").text = f"pp. {file_data.page}"

    # Titles
    used_trans = add_unittitle(
        file_did, file_data.title, database, file_data.date_string
    )

    if not used_trans:
        with open("outputs/missing_translations", "a", encoding="utf-8") as file:
            volume = parent_element.getchildren()[0].getchildren()[0].text  # type: ignore
            print(f"|{volume}.{file_data.page}|{file_data.title}", file=file)

    # Date
    date_data = create_date_data(file_data.date_string)
    add_unitdate(file_did, file_data.date_string, date_data)

    # Scopecontent
    scope = etree.SubElement(file_element, "scopecontent")
    chronlist = etree.SubElement(scope, "chronlist")
    chronitem = etree.SubElement(chronlist, "chronitem")
    add_dateset(chronitem, file_data.date_string, date_data)

    # Event
    event = etree.SubElement(chronitem, "event", {"localtype": "Document creation"})
    add_geognames(event, file_data.place, database)
    for identifier in re.findall(r"\$\w+", file_data.title):
        add_persname(event, identifier, database)

    # Daoset
    daoset = etree.SubElement(file_did, "daoset", {"coverage": "whole"})
    add_dao(daoset, file_data)

    return file_did, used_trans
