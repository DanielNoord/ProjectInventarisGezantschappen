import docx
from docx.shared import Pt

def write_list(list_of_lines):
    doc = docx.Document()
    for line in list_of_lines:
        paragraph = doc.add_paragraph(line)
        paragraph_format = paragraph.paragraph_format
        paragraph_format.first_line_indent = Pt(-10)
    doc.save("Lijst van namen.docx")
