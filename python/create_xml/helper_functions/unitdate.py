import lxml.etree as etree

def unitdate(parent_element, datestring, date1, date2, element_type):
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
