import os
import re

import lxml.etree as etree
from openpyxl import load_workbook

from functions.xml_create_elements import (
    basic_xml_file,
    volume_entry,
    dossier_entry,
    dossier_specific_file,
)

from functions.xlsx_parse import parse_file
from functions.xlsx_parse import parse_volume
from functions.xlsx_parse import parse_dossier


def create_xml_individual_files(localization, sheet, dossiers):
    print("test")
    # for file in files.split("\n"):
    #             f_pages, f_title, f_place, f_date = read_file(file)
    #             # Creates c04 level, might want to change
    #             dossier_specific_file(
    #                 c02, f_pages, f_title, f_place, f_date, localization
    #             )
    #     # Handle "Insteeksels"
    #     elif "." in d_number:
    #         pass

    #     else:
    #         raise Exception("This dossier is not handled correctly")


def create_xml_dossier(localization, sheet, v_num, c01):
    """Creates necessary dossier entries at the c02 level

    Args:
        localization (str): String indicating the localization of the inventory
        sheet (openpyxl.worksheet.worksheet.Worksheet): The .xlsx sheet with data
        v_num (str): Number of the volume
        c01 (lxml.etree._Element): The c01 element of the final .xml file
    """
    dossiers = {}

    # Find dossiers
    for cell in sheet["A"]:
        if cell.value is not None and (
            mat := re.search(r"ms.*?_(.*?)_.*?", cell.value)
        ):
            if mat.groups()[0] not in dossiers.keys():
                d_pages, d_title, d_data = parse_dossier(sheet, mat.groups()[0], v_num, cell)

                # Create entry
                dossiers[mat.groups()[0]] = dossier_entry(
                    c01,
                    v_num,
                    mat.groups()[0],
                    d_pages,
                    d_title,
                    d_data,
                    localization,
                )

    # Create dossier if no dossiers were found
    # TODO: Do we want to create a dossier in these cases?
    if dossiers == {}:
        dossiers[0] = dossier_entry(
                    c01,
                    v_num,
                    1,
                    "No page number",
                    "No dossier title",
                    "/",
                    localization,
                )

    create_xml_individual_files(localization, sheet, dossiers)


def create_xml_volume(localization, filename, archdesc):
    """Adds a volume to an 'archdesc' element

    Args:
        localization (str): String indicating the localization of the inventory
        filename (str): Name and directory of file
        archdesc (lxml.etree._Element): The archdesc element of the final .xml file
    """
    workbook = load_workbook(filename)
    first_sheet = workbook[workbook.sheetnames[0]]

    # Create volume entry at c01 level
    v_num, v_title, v_date = parse_volume(first_sheet[1])
    c01 = volume_entry(archdesc, v_num, v_title, v_date, localization)

    create_xml_dossier(localization, first_sheet, v_num, c01)

    print(f"Finished writing volume {v_num}")


def create_xml_file(localization, dir_name):
    """Creates and writes an xml file based on directory of volumes

    Args:
        localization (str): String indicating the localization of the inventory
        dir_name (str): Directory name
    """
    print("Starting to create XML file!")
    root, archdesc = basic_xml_file()

    directory = os.fsencode(f"{dir_name}{localization}")
    for file in sorted(os.listdir(directory)):
        filename = os.fsdecode(file)
        if not filename.count("~$") and filename.startswith("Final_"):
            create_xml_volume(
                localization, f"{dir_name}{localization}/{filename}", archdesc
            )

    tree = etree.ElementTree(root)

    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r"outputs"), exist_ok=True)
    tree.write(
        f"outputs/Inventaris_{localization}.xml",
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
        doctype="""<!DOCTYPE ead SYSTEM "http://www.nationaalarchief.nl/collectie/ead/ead.dtd">""",
    )

    print(f"Wrote file to outputs/Inventaris_{localization}.xml")
    print("Writing XML complete!")


if __name__ == "__main__":
    create_xml_file("it_IT", "inputs/VolumesExcelFilled/Final_")
