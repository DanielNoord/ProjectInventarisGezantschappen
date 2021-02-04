import docx
import re

def extract_volumes(filename):
    """Args:
        filename (str): File to be scanned

    Returns:
        [[str], [str], ...]: List of volumes found in the file
    """
    regex = re.compile(r".*?(Volume\n.*?)(?=Volume|$)", re.DOTALL)
    doc = docx.Document(filename)
    all_text = []
    for para in doc.paragraphs:
        all_text.append(para.text)
    full_text = '\n'.join(all_text)
    return re.findall(regex, full_text)
    