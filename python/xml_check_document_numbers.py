import os
from typing import TextIO

from lxml import etree


def match_daoset_ids(c01: etree._Element, volume_files: set[str]) -> None:
    """Checks all dao elements in a volume and checks if they can be found in
    a volume directory.

    Prints a warning if a file is never used.
    """
    with open("outputs/missing_files", "a", encoding="utf-8") as log:
        print(f"** Looking at MS{c01.find('did').find('unitid').text} **", file=log)  # type: ignore
        missing_files = set()
        for daoset in c01.iterdescendants("daoset"):  # type: ignore
            for dao in daoset.iterchildren():
                try:
                    volume_files.remove(dao.attrib["id"])
                except KeyError:
                    missing_files.add(dao.attrib["id"])
        if len(missing_files) != 0:
            print(
                "The following files (described in excel) are missing a scan:", file=log
            )
            for file_name in sorted(missing_files):
                print(file_name, file=log)
        if len(volume_files) != 0:
            print(
                "The following files (scans) are not covered by any dao (ID) in the XML database:",
                file=log,
            )
            for file_name in sorted(volume_files):
                print(file_name, file=log)


def get_files_in_volume_directory(volume: str, scans_directory: str) -> set[str]:
    """Gets a files in the volume directory of a certain volume name based on a base directory"""
    return set(os.listdir(os.path.join(scans_directory, f"MS{volume}")))


def traverse_c01_elements(database: TextIO, scans_directory: str) -> None:
    """Finds all c01 files in a xml file and traverses them"""
    # Create log file
    with open("outputs/missing_files", "w", encoding="utf-8") as log:
        log.writelines(
            "Overview of files currently not linking to excel description:\n"
        )

    xml_file = etree.parse(database)
    root = xml_file.getroot()
    archdesc = root.findall("archdesc")
    assert len(archdesc) == 1
    dsc = archdesc[0].findall("dsc")
    assert len(dsc) == 1
    for c01 in dsc[0].findall("c01"):
        did = c01.findall("did")
        assert len(did) == 1
        unitid = did[0].findall("unitid")
        assert len(unitid) == 1
        assert isinstance(unitid[0].text, str)
        volume_files = get_files_in_volume_directory(unitid[0].text, scans_directory)
        match_daoset_ids(c01, volume_files)


if __name__ == "__main__":
    with open("outputs/Legation_Archive.xml", encoding="utf-8") as file:
        traverse_c01_elements(file, "/Volumes/Seagate Basic Meda/VolumesLegazione")