import lxml.etree as etree
from helper_functions.extract_date import extract_date
from helper_functions.unitdate import unitdate


def dossier_specific_file(parent_element, pages, title, place, date, localization):
    c04 = etree.SubElement(parent_element, 'c04', level = "file")
    c04_did = etree.SubElement(c04, "did")
    c04_did_id = etree.SubElement(c04_did, 'unitid', type = "series_code")
    c04_did_id.text = f"pp. {pages}"
    c04_did_title = etree.SubElement(c04_did, 'unittitle')
    c04_did_title.text = title
    date1, date2 = extract_date(date, localization)
    unitdate(c04_did, date, date1, date2, "file")
