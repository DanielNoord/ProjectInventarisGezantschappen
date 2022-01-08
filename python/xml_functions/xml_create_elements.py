import re
from typing import Optional

from date_functions import create_date_data
from lxml import etree
from typing_utils import Database, FileData, SeriesData

from xml_functions.daoset import add_dao
from xml_functions.date_elements import add_dateset, add_unitdate
from xml_functions.person_elements import add_persname
from xml_functions.place_elements import add_geognames
from xml_functions.title_elements import add_unittitle


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


def series_entry(
    parent_element: etree._Element, series_data: SeriesData, database: Database
) -> tuple[etree._Element, Optional[re.Pattern[str]]]:
    """Returns an .xml element for a series at the c0X level"""
    series_level = "series"
    if series_data.level > 1:
        series_level = "subseries"
    serie_c = etree.SubElement(
        parent_element, f"c0{series_data.level}", level=series_level
    )
    serie_c_did = etree.SubElement(serie_c, "did")
    etree.SubElement(serie_c_did, "unitid").text = series_data.num

    used_trans = add_unittitle(
        serie_c_did, series_data.title, database, series_data.date, series_data.num
    )

    date_data = create_date_data(series_data.date)
    add_unitdate(serie_c_did, series_data.date, date_data)

    return serie_c, used_trans


def file_entry(
    parent_element: etree._Element,
    file_data: FileData,
    database: Database,
) -> tuple[etree._Element, Optional[re.Pattern[str]]]:
    """Creates an .xml element for a file within a dossier/volume"""
    file_element = etree.SubElement(
        parent_element, f"c0{file_data.series_level}", level="file"
    )
    file_did = etree.SubElement(file_element, "did")

    # ID
    etree.SubElement(file_did, "unitid").text = f"pp. {file_data.page}"

    # Titles
    used_trans = add_unittitle(
        file_did, file_data.title, database, file_data.date_string, file_data.file_name
    )

    if not used_trans:
        with open("outputs/missing_translations", "a", encoding="utf-8") as file:
            print(f"|{file_data.file_name}|{file_data.title}", file=file)

    # Date
    try:
        date_data = create_date_data(file_data.date_string)
    except ValueError as error:
        raise ValueError(f"{error.args[0]} for file {file_data.file_name}") from error
    add_unitdate(file_did, file_data.date_string, date_data)

    # Scopecontent
    scope = etree.SubElement(file_element, "scopecontent")
    chronlist = etree.SubElement(scope, "chronlist")
    chronitem = etree.SubElement(chronlist, "chronitem")
    add_dateset(chronitem, file_data.date_string, date_data)

    # Event
    event = etree.SubElement(chronitem, "event", {"localtype": "Document creation"})
    add_geognames(event, file_data.place, database, file_data.file_name)
    for identifier in re.findall(r"\$\w+", file_data.title):
        add_persname(event, identifier, database)

    # Daoset
    daoset = etree.SubElement(file_did, "daoset", {"coverage": "whole"})
    add_dao(daoset, file_data)

    return file_did, used_trans
