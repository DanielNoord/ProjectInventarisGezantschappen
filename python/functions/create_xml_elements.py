import lxml.etree as etree

from .helper_functions.extract_date import extract_date
from .helper_functions.unitdate import unitdate


def basic_xml_file():
    """Returns a basic .xml file based on EAD standard used for this project

    Returns:
        etree.Element: The root element of the .xml file
        etree.SubElement: The archdesc element of the .xml file
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
    titleproper.text = "Inventaris van het archieffonds van de Nederlandse Gezantschappen \
                            in Turijn en Rome, 1816 - 1874"
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
    language = """<langusage>This finding aid is written in
            <language langcode="dut" scriptcode="Latn"> Dutch</language>.
        </langusage>"""
    profiledesc.append(etree.fromstring(language))
    _ = etree.SubElement(profiledesc, "descrules")

    # Archdesc
    archdesc = etree.SubElement(root, "archdesc", level="fonds", type="inventory")
    archdescdid = etree.SubElement(archdesc, "did")
    _ = etree.SubElement(archdescdid, "unittitle")

    return root, archdesc


def dossier_entry(parent_element, v_number, number, _, title, date, localization):
    """Returns a dossier .xml element

    Args:
        parent_element (etree.Subelement): The element to which the dossier element is appended
        v_number (string): The volume number
        number (string): The dossier number
        pages (string): The pages of the dossier
        title (string): Title of the dossier
        date (string): Date of the dossier
        localization (string): The localization of the .xml file

    Returns:
        etree.SubElement: The dossier element at the c02 level
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
    unitdate(c02_did, date, date1, date2, "dossier")
    return c02


def dossier_specific_file(parent_element, pages, title, _, date, localization):
    """Returns an .xml element for a file within a dossier

    Args:
        parent_element (etree.Subelement): The element to which the file element is appended
        pages (string): The pages of the files
        title (string): Title of the file
        place (string): The place of the file
        date (string): Date of the file
        localization (string): The localization of the .xml file

    Returns:
        etree.SubElement: The dossier element at the c04 level
    """
    c04 = etree.SubElement(parent_element, "c04", level="file")
    c04_did = etree.SubElement(c04, "did")
    c04_did_id = etree.SubElement(c04_did, "unitid", type="series_code")
    c04_did_id.text = f"pp. {pages}"
    c04_did_title = etree.SubElement(c04_did, "unittitle")
    c04_did_title.text = title
    date1, date2 = extract_date(date, localization)
    unitdate(c04_did, date, date1, date2, "file")


def dossier_with_desc(parent_element, pages, title, _, date, localization):
    """Returns an .xml element for a dossier with description

    Args:
        parent_element (etree.Subelement): The element to which the dossier element is appended
        pages (string): The pages of the dossier
        title (string): Title of the dossier
        place (string): The place of the dossier
        date (string): Date of the dossier
        localization (string): The localization of the .xml file

    Returns:
        etree.SubElement: The dossier element at the c03 level
    """
    c03 = etree.SubElement(
        parent_element, "c03", otherlevel="filegrp", level="otherlevel"
    )
    c03_did = etree.SubElement(c03, "did")
    c03_did_id = etree.SubElement(c03_did, "unitid", type="series_code")
    c03_did_id.text = f"pp. {pages}"
    c03_did_title = etree.SubElement(c03_did, "unittitle")
    c03_did_title.text = title
    date1, date2 = extract_date(date, localization)
    unitdate(c03_did, date, date1, date2, "dossier")
    return c03


def volume_entry(parent_element, number, title, date, localization):
    """Returns an .xml element for a volume

    Args:
        parent_element (etree.Subelement): The element to which the dossier element is appended
        number (string): The number of the volume
        title (string): Title of the dossier
        date (string): Date of the dossier
        localization (string): The localization of the .xml file

    Returns:
        etree.SubElement: The dossier element at the c01 level
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
    unitdate(c01_did, date, date1, date2, "volume")
    return c01
