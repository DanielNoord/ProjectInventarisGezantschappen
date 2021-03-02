import docx


def extract_persons_and_identifiers(filename):
    """Args:
        filename (str): File to be scanned

    Returns:
        [[], [], [], ...] List of lists
            [string, string] Each list contains two strings which are:
                string: Data in inventaris
                string: Identifier given to that data
    """
    doc = docx.Document(filename)
    all_text = []
    for para in doc.paragraphs:
        if para.text == "":
            break
        all_text.append(para.text.split("\n"))
    return all_text
