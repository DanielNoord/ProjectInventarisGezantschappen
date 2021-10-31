import os
import re

FOLDER = "/Volumes/Seagate Basic Meda/VolumesLegazione/MS295"
PATTERN_TO_CHANGE = "MS295_b_"
PATTERN_TO_CHANGE_TO = "MS295_19_b_"
FIXED_PATTERN = r"(\d+)(.*)([rv].tif)"


def rename_files() -> None:
    """Rename files in a folder based on globals"""
    files = os.listdir(FOLDER)
    for file in files:
        if match := re.match(PATTERN_TO_CHANGE + FIXED_PATTERN, file):
            groups = match.groups()
            if int(groups[0]) > 0:
                os.rename(
                    f"{FOLDER}/{file}",
                    f"{FOLDER}/{PATTERN_TO_CHANGE_TO}{int(groups[0])}{groups[1]}{groups[2]}",
                )
    print("Rename complete!")


if __name__ == "__main__":
    rename_files()
