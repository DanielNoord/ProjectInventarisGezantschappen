import os
import re
import docx
from docx.shared import Pt


def write_list_to_be_translated(list_to_write, output_name):
    """ Write a docx file based on input. Adds two white lines after every entry.

    Args:
        list_to_write (list): List of translated names to be written, all in strings.
    """
    out_doc = docx.Document()
    for line in list_to_write:
        paragraph = out_doc.add_paragraph(f"{line}\n\n")

        # Add indentation
        paragraph_format = paragraph.paragraph_format
        paragraph_format.first_line_indent = Pt(-10)

    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r'outputs'), exist_ok=True)
    out_doc.save(f"outputs/Translated{output_name}.docx")