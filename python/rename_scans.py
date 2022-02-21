import os
import re


# pylint: disable-next=too-few-public-methods
class FileRenamer:
    """Renames files based on arguments."""

    def __init__(self, folder: str, old: str, new: str) -> None:
        self.filename_pattern = r"(\d+)(.*)([rv].tif)"
        """Pattern of the file names to match against."""

        self.folder = folder + old.split("_")[0]
        """Folder to scan."""

        self.old = old
        """Old filename pattern."""

        self.new = new
        """New filename pattern."""

        self.renamed = 0
        """Amount of renamed files."""

    def rename_files(self) -> None:
        """Rename files in a folder based on attributes."""
        for file in os.listdir(self.folder):
            sanitized_file = (
                file.replace("rbis", "bisr")
                .replace("vbis", "bisv")
                .replace("_r.tif", "r.tif")
                .replace("_v.tif", "v.tif")
            )
            if match := re.match(self.old + self.filename_pattern, sanitized_file):
                groups = match.groups()
                if int(groups[0]) > 0:
                    os.rename(
                        f"{self.folder}/{file}",
                        f"{self.folder}/{self.new}{int(groups[0])}{groups[1]}{groups[2]}",
                    )
                    self.renamed += 1
        print("Rename complete!")
        print(f"Renamed {self.renamed} files.")


if __name__ == "__main__":
    renamer = FileRenamer(
        "/Users/daniel/DocumentenLaptop/MEGA/",
        "MS278_",
        "MS278_3_",
    )
    renamer.rename_files()
