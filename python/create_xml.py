import lxml.etree as etree
import helper_functions

def basic_xml_file():
    root = etree.Element("ead")

    # Eadheader
    eadheader = etree.SubElement(root, "eadheader")
    eaddid = etree.SubElement(eadheader, "eadid")
    comment = etree.Comment('Nationaal Archief')
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
    date = etree.SubElement(publicationstmt, "date", calendar = "gregorian",\
        era = "ce", normal = "2021")
    date.text = "(c) 2021"
    para = etree.SubElement(publicationstmt, "p", id = "copyright")
    extref = etree.SubElement(para, "extref", linktype = "simple",\
        href = "http://creativecommons.org/publicdomain/zero/1.0/",\
        actuate = "onrequest", show = "new")
    extref.text = "cc0"

    # Profiledesc
    profiledesc = etree.SubElement(eadheader, "profiledesc")
    language = """<langusage>This finding aid is written in
            <language langcode="dut" scriptcode="Latn"> Dutch</language>.
        </langusage>"""
    profiledesc.append(etree.fromstring(language))
    descrules = etree.SubElement(profiledesc, "descrules")

    # Archdesc
    archdesc = etree.SubElement(root, "archdesc", level = "fonds", type = "inventory")
    archdescdid = etree.SubElement(archdesc, "did")
    unittitle = etree.SubElement(archdescdid, "unittitle")

    return root, archdesc

def volume_entry(parent_element, number, title, date, localization):
    desc = etree.SubElement(parent_element, "dsc")
    head = etree.SubElement(desc, "head")
    head.text = f"{number} {title}"
    c01 = etree.SubElement(desc, 'c01', level = "series")
    c01_did = etree.SubElement(c01, "did")
    c01_did_id = etree.SubElement(c01_did, 'unitid', type = "series_code")
    c01_did_id.text = number + "."
    c01_did_title = etree.SubElement(c01_did, 'unittitle')
    c01_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    create_unitdate(c01_did, date, date1, date2, "volume")
    return c01

def dossier_entry(parent_element, v_number, number, pages, title, date, localization):
    c02 = etree.SubElement(parent_element, 'c02', level = "subseries")
    c02_head = etree.SubElement(c02, "head")
    c02_head.text = title
    c02_did = etree.SubElement(c02, "did")
    c02_did_id = etree.SubElement(c02_did, 'unitid', type = "series_code")
    c02_did_id.text = f"{v_number}.{number}"
    c02_did_title = etree.SubElement(c02_did, 'unittitle')
    c02_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    create_unitdate(c02_did, date, date1, date2, "dossier")
    return c02

def dossier_with_desc(parent_element, pages, title, place, date, localization):
    c03 = etree.SubElement(parent_element, 'c03', otherlevel = "filegrp", level = "otherlevel")
    c03_did = etree.SubElement(c03, "did")
    c03_did_id = etree.SubElement(c03_did, 'unitid', type = "series_code")
    c03_did_id.text = f"pp. {pages}"
    c03_did_title = etree.SubElement(c03_did, 'unittitle')
    c03_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    create_unitdate(c03_did, date, date1, date2, "dossier")
    return c03

def dossier_specific_file(parent_element, pages, title, place, date, localization):
    c04 = etree.SubElement(parent_element, 'c04', level = "file")
    c04_did = etree.SubElement(c04, "did")
    c04_did_id = etree.SubElement(c04_did, 'unitid', type = "series_code")
    c04_did_id.text = f"pp. {pages}"
    c04_did_title = etree.SubElement(c04_did, 'unittitle')
    c04_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    create_unitdate(c04_did, date, date1, date2, "file")

def create_unitdate(parent_element, datestring, date1, date2, element_type):
    """ Creates and appends an unitdate element

    Args:
        parent_element (etree.SubElement): The element to attacht the unitdate element to
        datestring (string): The full date in standard format xxxx-xx-xx/xxxx-xx-xx
        date1 (string): The begin date in text format (i.e., 1 januari 2021)
        date2 (string): The end date in text format (i.e., 2 januari 2021)
        element_type (string): The type of date (i.e., file, volume or function/job)
    """
    if not datestring:
        return
    udate_element = etree.SubElement(parent_element, 'unitdate', calendar = "gregorian",\
        era = "ce", normal = datestring)
    if element_type:
        if date1:
            if date2:
                udate_element.text = f"{date1} tot en met {date2}"
            else:
                udate_element.text = f"{date1}"
        elif date2:
            udate_element.text = f"Tot en met {date2}"
            raise Exception("This element only has an end date. Check if this is correct!")
