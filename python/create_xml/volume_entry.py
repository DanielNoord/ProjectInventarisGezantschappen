import lxml.etree as etree
from helper_functions.extract_date import extract_date
from helper_functions.unitdate import unitdate

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
    date1, date2 = extract_date(date, localization)
    unitdate(c01_did, date, date1, date2, "volume")
    return c01
