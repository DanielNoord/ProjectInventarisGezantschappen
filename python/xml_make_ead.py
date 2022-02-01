#!/usr/bin/env python3

import os
import re
from typing import cast

import openpyxl
from lxml import etree
from openpyxl import load_workbook

from data_parsing import initialize_database_for_xml
from typing_utils import Database
from xlsx_functions import compare_rows, parse_file, parse_series
from xlsx_make import create_sanitized_xlsx
from xml_functions import add_dao, basic_xml_file, file_entry, fix_daoset, series_entry


# pylint: disable-next=too-few-public-methods
class EADMaker:
    """Class which can a EAD compliant .xml file."""

    def __init__(self, input_dir: str, sanitize: bool = True) -> None:
        self.input_dir = input_dir
        """Directory with input .xlsx files."""

        self.sanitized_dir = input_dir.replace("inputs", "outputs").replace(
            "VolumesExcel", "VolumesExcelSanitized"
        )
        """Directory with input .xlsx files."""

        self.log_missing_translations = "outputs/missing_translations"
        """Filename of the log file used to track missing translations."""

        self.log_missing_titles = "outputs/missing_titles"
        """Filename of the log file used to track missing titles."""

        self.log_missing_placenames = "outputs/missing_placenames"
        """Filename of the log file used to track missing placenames."""

        self.log_title_errors = "outputs/title_errors"
        """Filename of the log file used to track errors in document titles."""

        self.log_xml_errors = "outputs/xml_errors"
        """Filename of the log file used to track errors in the xml file."""

        self._create_logging_files()

        # Sanitize the input .xlsx files
        if sanitize:
            create_sanitized_xlsx(input_dir)

    def create_ead(self) -> None:
        create_xml_file(self.sanitized_dir)

    def _create_logging_files(self) -> None:
        """Create some files to store messages during the creation process."""
        with open(self.log_missing_translations, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Missing translations |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_missing_titles, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Missing titles |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_missing_placenames, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Missing placenames |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_title_errors, "w", encoding="utf-8") as file:
            file.writelines(
                "|no.  |Errors in titles |\n" "| ------------- | ------------- |\n"
            )
        with open(self.log_xml_errors, "w", encoding="utf-8") as file:
            file.writelines("")


def create_xml_individual_files(  # pylint: disable=too-many-branches
    sheet: openpyxl.worksheet.worksheet.Worksheet,
    series: dict[str, etree._Element],
    database: Database,
) -> set[re.Pattern[str]]:
    """Based on a sheet creates .xml entries for every file found"""
    prev_file, prev_file_did, prev_series = None, None, None
    used_trans: set[re.Pattern[str]] = set()

    for file in sheet.iter_rows():
        similar = False
        # Skip empty lines or series title lines
        if file[0].value is None or file[0].value.endswith("_title"):
            continue

        # Error on files with a space in their "file number"
        if " " in file[0].value:
            raise ValueError(
                f"There is a space in the file number {file[0].value}. This is not allowed!"
            )

        file_data = parse_file(file)

        if (
            prev_file is not None
            and prev_file_did is not None
            and file_data.series == prev_series
            and file_data.title != "Bianca"
        ):
            similar = compare_rows(file, prev_file)

        # If current file is a verso description, remove verso from previous daoset
        if re.match(r".+v", file_data.file_name):
            if prev_file_did is None:
                raise ValueError(
                    # pylint: disable-next=line-too-long
                    f"{file_data.file_name} is a verso appearing before the description of {file_data.file_name[:-1]}"
                )
            for dao in prev_file_did.find("daoset"):
                if dao.attrib["id"] == f"{file_data.file_name}.tif":
                    dao.getparent().remove(dao)

        if not similar:
            prev_file_did, used_trans_update = file_entry(
                series[file_data.series], file_data, database
            )
        # Update pages/id of previous document
        else:
            # If similar means prev_file_did is defined
            prev_file_did = cast(
                etree._Element, prev_file_did  # pylint: disable=protected-access
            )
            unitid = prev_file_did.find("unitid")
            if (
                not isinstance(
                    unitid, etree._Element  # pylint: disable=protected-access
                )
                or not unitid.text
                or not isinstance(unitid.text, str)
            ):
                raise ValueError(
                    f"Can't find unitid in {prev_file_did}, it is empty or it isn't a string"
                )
            if "-" in unitid.text:
                unitid.text = unitid.text[: unitid.text.index("-") + 1] + file_data.page
            else:
                unitid.text += f"-{file_data.page}"

            # Update daoset of previous document
            daoset = prev_file_did.find("daoset")
            if not isinstance(
                daoset, etree._Element  # pylint: disable=protected-access
            ):
                raise ValueError(f"Can't find daoset in {prev_file_did}")
            add_dao(daoset, file_data)

        prev_file = file
        prev_series = file_data.series
        if used_trans_update:
            used_trans.add(used_trans_update)

    return used_trans


def create_xml_series(
    filename: str, archdesc: etree._Element, database: Database
) -> tuple[dict[str, dict[str, etree._Element]], set[re.Pattern[str]]]:
    """Adds a volume to an 'archdesc' element"""
    workbook = load_workbook(filename)
    first_sheet = workbook[workbook.sheetnames[0]]
    used_translations: set[re.Pattern[str]] = set()
    sub_levels: dict[str, etree._Element] = {}

    for index, cell in enumerate(first_sheet["A"]):
        if match := re.match("(.*)_title", cell.value or ""):
            series_data = parse_series(first_sheet[index + 1])
            if series_data.level == 1:
                sub_levels[match.groups()[0]], used_trans_series = series_entry(
                    archdesc, series_data, database
                )
            else:
                if not (parent_level := re.match(r"(.*)_.*?", match.groups()[0])):
                    raise ValueError(
                        f"Can't determine the series parent of {cell.value}."
                        "Does it have the correct format?"
                    )
                sub_levels[match.groups()[0]], used_trans_series = series_entry(
                    sub_levels[parent_level.groups()[0]], series_data, database
                )
            if used_trans_series:
                used_translations.add(used_trans_series)

    used_trans_dos = create_xml_individual_files(first_sheet, sub_levels, database)

    used_translations.update(used_trans_dos)

    if not (volume_number := re.match("(.*)_title", first_sheet["A"][0].value)):
        raise ValueError(
            f"Can't determine the volume/ms number of {first_sheet['A'][0].value}."
            "Does it have the correct format?"
        )
    print(f"""Finished writing volume {volume_number.groups()[0]}\n""")

    return {str(volume_number.groups()[0]): sub_levels}, used_translations


def create_xml_file(dir_name: str) -> None:
    """Creates and writes an xml file based on directory of volumes"""
    print("Starting to create XML file!")
    database = initialize_database_for_xml()
    series: dict[str, dict[str, etree._Element]] = {}
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
        series_update, used_translations_update = create_xml_series(
            f"{dir_name}/{file}", archdesc_dsc, database
        )
        series.update(series_update)
        used_translations.update(used_translations_update)

    fix_daoset(root)

    tree = etree.ElementTree(root)

    # Check if outputs directory exists and then write file
    os.makedirs(os.path.join(os.getcwd(), r"outputs"), exist_ok=True)
    tree.write(  # type: ignore[call-arg] # Stub doesn't recognize doctype parameter is valid
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
    for i in series.values():
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
        # pylint: disable-next=line-too-long
        "xmllint --noout --dtdvalid outputs/ead3.dtd outputs/Legation_Archive.xml 2> outputs/xml_errors"
    )
    print("XML-DTD check complete!")


if __name__ == "__main__":
    eadmaker = EADMaker(
        "inputs/VolumesExcel/it_IT",
        True,
    )
    eadmaker.create_ead()
