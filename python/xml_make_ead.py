#!/usr/bin/env python3

import os
import re

import openpyxl
from lxml import etree
from openpyxl import load_workbook

from data_parsing import initialize_database_for_xml
from typing_utils import Database
from xlsx_functions import compare_rows, parse_dossier, parse_file, parse_volume
from xlsx_make import create_sanitized_xlsx
from xml_functions import basic_xml_file, dossier_entry, file_entry, volume_entry


def create_xml_individual_files(
    sheet: openpyxl.worksheet.worksheet.Worksheet,
    dossiers: dict[str, etree._Element],
    vol_entry: etree._Element,
    database: Database,
) -> set[re.Pattern[str]]:
    """Based on a sheet creates .xml entries for every file found"""
    prev_file, prev_file_did, similar = None, None, None
    used_trans: set[re.Pattern[str]] = set()

    for file in sheet.iter_rows():
        if file[0].value is None:
            continue
        if " " in file[0].value:
            raise ValueError(
                f"There is a space in the file number {file[0].value}. This is not allowed!"
            )
        if not file[0].value.endswith("_title"):
            if prev_file is not None and prev_file_did is not None:
                similar = compare_rows(file, prev_file)

            file_data = parse_file(file)

            if not similar:
                # Check if file belongs to a dossier
                try:
                    if mat := re.search(r"ms.+?_(.+?)_.+?", file[0].value):
                        prev_file_did, used_trans_update = file_entry(
                            dossiers[mat.groups()[0]], file_data, database
                        )
                    else:
                        prev_file_did, used_trans_update = file_entry(
                            vol_entry, file_data, database
                        )
                except ValueError as error:
                    raise ValueError(
                        f"{file[0].value} gives following error: {error}"
                    ) from error
            else:
                # Update pages/id of previous document
                unitid = prev_file_did.find("unitid")
                if "-" in unitid.text:
                    unitid.text = (
                        unitid.text[: unitid.text.index("-") + 1] + file_data.page
                    )
                else:
                    unitid.text += f"-{file_data.page}"

                # Update daoset of previous document
                daoset = prev_file_did.find("daoset")
                etree.SubElement(
                    daoset,
                    "dao",
                    {
                        "coverage": "part",
                        "daotype": "derived",
                        "id": f"{file_data.file_name}r.tif",
                    },
                )
                etree.SubElement(
                    daoset,
                    "dao",
                    {
                        "coverage": "part",
                        "daotype": "derived",
                        "id": f"{file_data.file_name}v.tif",
                    },
                )
            prev_file = file
            if used_trans_update:
                used_trans.add(used_trans_update)

    return used_trans


def create_xml_dossier(
    sheet: openpyxl.worksheet.worksheet.Worksheet,
    v_num: str,
    c01: etree._Element,
    database: Database,
) -> tuple[set[str], set[re.Pattern[str]]]:
    """Creates necessary dossier entries at the c02 level"""
    dossiers: dict[str, etree._Element] = {}
    used_trans: set[re.Pattern[str]] = set()

    # Find dossiers
    for cell in sheet["A"]:
        if cell.value is not None and (
            mat := re.search(r"ms.+?_(.+?)_.+?", cell.value)
        ):
            if mat.groups()[0] not in dossiers.keys():
                d_title, d_date = parse_dossier(sheet, mat.groups()[0], v_num, cell)

                # Create entry
                dossiers[mat.groups()[0]], pattern = dossier_entry(
                    c01, v_num, mat.groups()[0], d_title, d_date, database
                )

                if pattern:
                    used_trans.add(pattern)

    used_trans.update(create_xml_individual_files(sheet, dossiers, c01, database))

    if not dossiers:
        return {v_num}, used_trans
    return {f"{v_num}_{i}" for i in dossiers}, used_trans


def create_xml_volume(
    filename: str, archdesc: etree._Element, database: Database
) -> tuple[dict[str, set[str]], set[re.Pattern[str]]]:
    """Adds a volume to an 'archdesc' element"""
    workbook = load_workbook(filename)
    first_sheet = workbook[workbook.sheetnames[0]]
    used_translations: set[re.Pattern[str]] = set()

    # Create volume entry at c01 level
    volume_data = parse_volume(first_sheet[1])
    c01, used_trans_vol = volume_entry(archdesc, volume_data, database)

    dossiers, used_trans_dos = create_xml_dossier(
        first_sheet, volume_data.num, c01, database
    )

    if used_trans_vol:
        used_translations.add(used_trans_vol)
    used_translations.update(used_trans_dos)

    print(f"""Finished writing volume {volume_data.num}\n""")

    return {volume_data.num: dossiers}, used_translations


def create_xml_file(dir_name: str) -> None:
    """Creates and writes an xml file based on directory of volumes"""
    print("Starting to create XML file!")
    database = initialize_database_for_xml()
    dossiers: dict[str, set[str]] = {}
    used_translations: set[re.Pattern[str]] = set()

    root, archdesc_dsc = basic_xml_file()

    # Iterate files sorted by volume number
    files = [i for i in os.listdir(dir_name) if i.startswith("Paesi")]
    for file in sorted(
        files,
        key=lambda name: int(
            name.replace("Paesi Bassi VOLUME ", "").replace("_it_IT.xlsx", "")
        ),
    ):
        dossiers_update, used_translations_update = create_xml_volume(
            f"{dir_name}/{file}", archdesc_dsc, database
        )
        dossiers.update(dossiers_update)
        used_translations.update(used_translations_update)

    tree = etree.ElementTree(root)

    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r"outputs"), exist_ok=True)
    tree.write(  # type: ignore # Stub doesn't recognize doctype parameter is valid
        "outputs/Legation_Archive.xml",
        pretty_print=True,
        xml_declaration=True,
        encoding="UTF-8",
        doctype="""<!DOCTYPE ead PUBLIC "+// http://ead3.archivists.org/schema/ //DTD ead3 (Encoded Archival Description (EAD) Version 3)//EN" "ead3.dtd">""",  # pylint: disable=line-too-long
    )

    print("Printed file to outputs/Legation_Archive.xml")
    print("Writing XML complete!")

    # Printing some descriptive stats
    print("Found the following dossiers:")
    for i in dossiers.values():
        print(", ".join(i))
    print("Found the following unused translations:")
    print(
        "\n".join(
            i.pattern
            for i in database.document_titles.keys()
            if i not in used_translations
        )
    )

    os.system(
        "xmllint --noout --dtdvalid outputs/ead3.dtd outputs/Legation_Archive.xml 2> outputs/xml_errors"
    )
    print("XML-DTD check complete!")


def create_output_files() -> None:
    """Creates some files to store messages during the creation process"""
    with open("outputs/missing_translations", "w", encoding="utf-8") as file:
        file.writelines(
            "|no.  |Missing translations |\n" "| ------------- | ------------- |\n"
        )
    with open("outputs/missing_titles", "w", encoding="utf-8") as file:
        file.writelines(
            "|no.  |Missing titles |\n" "| ------------- | ------------- |\n"
        )
    with open("outputs/missing_placenames", "w", encoding="utf-8") as file:
        file.writelines(
            "|no.  |Missing placenames |\n" "| ------------- | ------------- |\n"
        )
    with open("outputs/title_errors", "w", encoding="utf-8") as file:
        file.writelines(
            "|no.  |Errors in titles |\n" "| ------------- | ------------- |\n"
        )
    with open("outputs/xml_errors", "w", encoding="utf-8") as file:
        file.writelines("")


if __name__ == "__main__":
    create_output_files()
    create_sanitized_xlsx("inputs/VolumesExcel/it_IT")
    create_xml_file("outputs/VolumesExcelSanitized/it_IT")
