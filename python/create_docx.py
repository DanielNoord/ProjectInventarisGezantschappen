import docx
import os
from docx.shared import Pt

def write_list(list_of_lines):
    doc = docx.Document()
    for line in list_of_lines:
        paragraph = doc.add_paragraph(line)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.first_line_indent = Pt(-10)
    
    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r'outputs'), exist_ok=True)
    doc.save("outputs/Namenlijst.docx")
