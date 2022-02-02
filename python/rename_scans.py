import os
import re


# pylint: disable-next=too-few-public-methods
class FileRenamer:
    """Renames files based on arguments."""

    def __init__(self, old: str, new: str) -> None:
        self.filename_pattern = r"(\d+)(.*)([rv].tif)"
        """Pattern of the file names to match against."""

        self.folder = (
            "/Volumes/Seagate Basic Media/VolumesLegazione/" + old.split("_")[0]
        )
        """Folder to scan."""

        self.old = old
        """Old filename pattern."""

        self.new = new
        """New filename pattern."""

    def rename_files(self) -> None:
        """Rename files in a folder based on attributes."""
        for file in os.listdir(self.folder):
            sanitized_file = file.replace("rbis", "bisr").replace("vbis", "bisv")
            sanitized_file = file.replace("_r.tif", "r.tif").replace("_v.tif", "v.tif")
            if "MS284_11_1_193_" in sanitized_file:
                sanitized_file = sanitized_file.replace(
                    "MS284_11_1_193_", "MS284_11_193"
                )
            if match := re.match(self.old + self.filename_pattern, sanitized_file):
                groups = match.groups()
                if int(groups[0]) > 0:
                    os.rename(
                        f"{self.folder}/{file}",
                        f"{self.folder}/{self.new}{int(groups[0])}{groups[1]}{groups[2]}",
                    )
        print("Rename complete!")


if __name__ == "__main__":
    renamer = FileRenamer(
        "MS285_12_2_",
        "MS285_12_b_",
    )
    renamer.rename_files()
