import lxml.etree as etree
from helper_functions.extract_date import extract_date
from helper_functions.unitdate import unitdate


def dossier_entry(parent_element, v_number, number, pages, title, date, localization):
    c02 = etree.SubElement(parent_element, 'c02', level = "subseries")
    c02_head = etree.SubElement(c02, "head")
    c02_head.text = title
    c02_did = etree.SubElement(c02, "did")
    c02_did_id = etree.SubElement(c02_did, 'unitid', type = "series_code")
    c02_did_id.text = f"{v_number}.{number}"
    c02_did_title = etree.SubElement(c02_did, 'unittitle')
    c02_did_title.text = title
    date1, date2 = extract_date(date, localization)
    unitdate(c02_did, date, date1, date2, "dossier")
    return c02
