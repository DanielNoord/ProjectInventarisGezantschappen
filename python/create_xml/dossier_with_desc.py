import lxml.etree as etree
from helper_functions.extract_date import extract_date
from helper_functions.unitdate import unitdate


def dossier_with_desc(parent_element, pages, title, place, date, localization):
    c03 = etree.SubElement(parent_element, 'c03', otherlevel = "filegrp", level = "otherlevel")
    c03_did = etree.SubElement(c03, "did")
    c03_did_id = etree.SubElement(c03_did, 'unitid', type = "series_code")
    c03_did_id.text = f"pp. {pages}"
    c03_did_title = etree.SubElement(c03_did, 'unittitle')
    c03_did_title.text = title
    date1, date2 = extract_date(date, localization)
    unitdate(c03_did, date, date1, date2, "dossier")
    return c03
