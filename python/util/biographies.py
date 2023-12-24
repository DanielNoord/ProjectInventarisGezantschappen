import json
import os
from pathlib import Path

from util.get_file import maybe_open_file


def export_biographies(print_to_file: bool) -> None:
    """Export all biographies using the file name as agreed upon."""
    with open(Path("inputs") / "Biographies.json", encoding="utf-8") as file:
        data = json.load(file)
    data.pop("$schema")

    os.makedirs("outputs/biographies", exist_ok=True)
    for identifier, biographies in data.items():
        for locale, bio in biographies.items():
            if not bio:
                continue

            with maybe_open_file(
                should_open_file=print_to_file,
                name=Path("outputs") / "biographies" / f"{identifier[1:]}_{locale}.txt",
            ) as file:
                print(bio, file=file)
