import lxml.etree as etree
import helper_functions
import re

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
    titleproper.text = "Archieffonds Nederlandse Legatie in Turijn en Rome, 1816 - 1874"
    author = titleproper = etree.SubElement(titlestmt, "author")
    author.text = "D.M. van Noord"
    publicationstmt = etree.SubElement(filedesc, "publicationstmt")
    publisher = etree.SubElement(publicationstmt, "publisher")
    publisher.text = "KNIR"
    date = etree.SubElement(publicationstmt, "date", calendar = "gregorian", era = "ce", normal = "2021")
    date.text = "2021"
    para = etree.SubElement(publicationstmt, "p", id = "copyright")
    extref = etree.SubElement(para, "extref", linktype = "simple", href = "http://creativecommons.org/publicdomain/zero/1.0/",\
        actuate = "onrequest", show = "new")
    extref.text = "cc0"
    
    # Profiledesc
    profiledesc = etree.SubElement(eadheader, "profiledesc")
    language = """<langusage>This finding aid is written in 
            <language langcode="dut" scriptcode="Latn">Dutch</language>.
        </langusage>"""
    profiledesc.append(etree.fromstring(language))
    descrules = etree.SubElement(profiledesc, "descrules")

    # Archdesc
    archdesc = etree.SubElement(root, "archdesc", level = "fonds", type = "inventory")
    archdescdid = etree.SubElement(archdesc, "did")
    unittitle = etree.SubElement(archdescdid, "unittitle")
    
    return root, archdesc

def volume_entry(number, title, date, parent_element, localization):
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
    c01_did_date = etree.SubElement(c01_did, 'unitdate', calendar = "gregorian",\
        era = "ce", normal = date)
    c01_did_date.text = f"{date1} tot en met {date2}"
    return c01

def dossier_entry(v_number, number, pages, title, date, parent_element, localization):
    c02 = etree.SubElement(parent_element, 'c02', level = "subseries")
    c02_head = etree.SubElement(c02, "head")
    c02_head.text = title
    c02_did = etree.SubElement(c02, "did")
    c02_did_id = etree.SubElement(c02_did, 'unitid', type = "series_code")
    c02_did_id.text = f"{v_number}.{number}"
    c02_did_title = etree.SubElement(c02_did, 'unittitle')
    c02_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    c02_did_date = etree.SubElement(c02_did, 'unitdate', calendar = "gregorian",\
        era = "ce", normal = date)
    c02_did_date.text = f"{date1} tot en met {date2}"
    return c02

def dossier_with_desc(pages, title, place, date, parent_element, localization):
    c03 = etree.SubElement(parent_element, 'c03', otherlevel = "filegrp", level = "otherlevel")
    c03_did = etree.SubElement(c03, "did")
    c03_did_id = etree.SubElement(c03_did, 'unitid', type = "series_code")
    c03_did_id.text = f"pp. {pages}"
    c03_did_title = etree.SubElement(c03_did, 'unittitle')
    c03_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    c03_did_date = etree.SubElement(c03_did, 'unitdate', calendar = "gregorian",\
        era = "ce", normal = date)
    c03_did_date.text = f"{date1} tot en met {date2}"
    return c03

def dossier_specific_file(pages, title, place, date, parent_element, localization):
    c04 = etree.SubElement(parent_element, 'c04', level = "file")
    c04_did = etree.SubElement(c04, "did")
    c04_did_id = etree.SubElement(c04_did, 'unitid', type = "series_code")
    c04_did_id.text = f"pp. {pages}"
    c04_did_title = etree.SubElement(c04_did, 'unittitle')
    c04_did_title.text = title
    date1, date2 = helper_functions.extract_date(date, localization)
    c04_did_date = etree.SubElement(c04_did, 'unitdate', calendar = "gregorian",\
        era = "ce", normal = date)
    c04_did_date.text = f"{date1} tot en met {date2}"