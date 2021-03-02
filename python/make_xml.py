import os

import lxml.etree as etree

from create_xml.basic_xml_file import basic_xml_file
from create_xml.dossier_entry import dossier_entry
from create_xml.dossier_specific_file import dossier_specific_file
from create_xml.dossier_with_desc import dossier_with_desc
from create_xml.volume_entry import volume_entry
from parse_docx.dossier import dossier as read_dossier
from parse_docx.file import file as read_file
from parse_docx.split_into_dossiers import \
    split_into_dossiers as read_split_into_dossiers
from parse_docx.sub_dossier_description import \
    sub_dossier_description as read_sub_dossier_description
from parse_docx.sub_series import sub_series as read_sub_series
from parse_docx.volume import volume as read_volume
from read_docx.extract_volumes import extract_volumes


def write_xml_file(localization, filename):
    """Writes an EAD compliant .xml file

    Args:
        localization (str): Language of the output file ("nl_NL", "it_IT", "en_GB")
        filename (str): Name of the input file

    Raises:
        Exception: Whenever an dossier is encountered that is not understood
    """
    print("Starting to create XML file!")
    root, archdesc = basic_xml_file()

    # Parse and create volume entries
    for volume in extract_volumes(filename):
        v_number, v_title, v_date = read_volume(volume)

        # TODO: These volumes are incorrect
        if v_number in ["301", "302", "303", "306"] or int(v_number) > 306:
            continue

        # c01 is the c01-level entry for the volume
        c01 = volume_entry(archdesc, v_number, v_title, v_date, localization)

        for dossier in read_split_into_dossiers(volume):
            # Create dossier entry
            d_number, d_pages, d_title, d_date,\
                d_serie_desc, files = read_dossier(dossier)
            c02 = dossier_entry(c01, v_number, d_number, d_pages,\
                d_title, d_date, localization)

            # TODO: For debug purposes
            print(v_number, d_number, d_title)

            # Handle sub-series in dossiers
            if d_serie_desc:
                for sub_serie in read_sub_series(d_serie_desc):
                    d_d_pages, d_d_title, d_d_place, d_d_date =\
                       read_sub_dossier_description(sub_serie[0])
                    c03 = dossier_with_desc(c02, d_d_pages, d_d_title, d_d_place,\
                        d_d_date, localization)
                    if sub_serie[1]:
                        for file in sub_serie[2].split("\n"):
                            f_pages, f_title, f_place, f_date = read_file(file)
                            dossier_specific_file(c03, f_pages, f_title, f_place,\
                                f_date, localization)

            # If there are only files and no sub-series
            elif files:
                for file in files.split("\n"):
                    f_pages, f_title, f_place, f_date = read_file(file)
                    # Creates c04 level, might want to change
                    dossier_specific_file(c02, f_pages, f_title,\
                        f_place, f_date, localization)

            # Handle "Insteeksels"
            elif "." in d_number:
                pass

            else:
                raise Exception("This dossier is not handled correctly")

    tree = etree.ElementTree(root)

    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r'outputs'), exist_ok=True)
    tree.write(
        f"outputs/Inventaris_{localization}.xml",
        pretty_print=True,
        xml_declaration = True,
        encoding = 'UTF-8',
        doctype='''<!DOCTYPE ead SYSTEM "http://www.nationaalarchief.nl/collectie/ead/ead.dtd">''')

    print("Writing XML complete!")

if __name__ == "__main__":
    write_xml_file("nl_NL", "inputs/Fonds Nederlandse Gezantschappen.docx")
