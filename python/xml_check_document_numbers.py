import os
from typing import TextIO

from lxml import etree


def match_daoset_ids(c01: etree._Element, volume_files: set[str]) -> None:
    """Checks all dao elements in a volume and checks if they can be found in.

    a volume directory.

    Prints a warning if a file is never used.
    """
    with open("outputs/missing_files", "a", encoding="utf-8") as log:
        missing_files = set()
        for dao in c01.iterdescendants("dao"):
            try:
                volume_files.remove(str(dao.attrib["href"]))
            except KeyError:
                missing_files.add(dao.attrib["href"])

        # The scans contain some temporary files
        volume_files = {i for i in volume_files if "/._" not in i}

        if missing_files or volume_files:
            print(f"\n** Controlling MS{c01.find('did').find('unitid').text} **", file=log)  # type: ignore[union-attr]

        if missing_files:
            print(
                "The following files are described in excel but do not have an associated scan:",
                file=log,
            )
            print(
                "I seguenti file sono descritti in Excel ma non hanno una scansione associata:",
                file=log,
            )
            for file_name in sorted(missing_files):
                print(f" - {file_name!r}", file=log)

        if volume_files:
            print(
                "The following files exist as scan but are not described in excel:",
                file=log,
            )
            print(
                "I seguenti file esistono come scansione ma non sono descritti in excel:",
                file=log,
            )
            for file_name in sorted(volume_files):
                print(f" + {file_name}", file=log)

        assert not missing_files, missing_files
        assert not volume_files, volume_files


def get_files_in_volume_directory(volume: str, scans_directory: str) -> set[str]:
    """Gets a files in the volume directory of a certain volume name based on a base directory."""
    return {
        f"VolumesLegazione/MS{volume}/{i}"
        for i in os.listdir(os.path.join(scans_directory, f"MS{volume}"))
    }


def traverse_c01_elements(
    database: TextIO, scans_directory: str, use_prestored_names: bool
) -> None:
    """Finds all c01 files in a xml file and traverses them."""
    # Create log file
    with open("outputs/missing_files", "w", encoding="utf-8") as log:
        log.write("")

    if use_prestored_names:
        with open("inputs/ScanFiles.txt", encoding="utf-8") as scans_file:
            scans = scans_file.readlines()

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
        if not use_prestored_names:
            volume_files = get_files_in_volume_directory(unitid[0].text, scans_directory)
        else:
            volume_files = {i.replace("\n", "") for i in scans if f"MS{unitid[0].text}" in i}
        volume_files.discard(f"VolumesLegazione/MS{unitid[0].text}/.DS_Store")
        match_daoset_ids(c01, volume_files)


if __name__ == "__main__":
    with open("outputs/Legation_Archive.xml", encoding="utf-8") as file:
        traverse_c01_elements(
            file,
            "/Volumes/LaCie/VolumesLegazione",
            False,
        )
