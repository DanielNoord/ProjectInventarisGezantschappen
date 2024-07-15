import json
import os
from typing import Any


def write_single_json_file(data: dict[str, Any], file_directory: str, file_name: str) -> None:
    """Write a dict to json file while checking for non-existing directories."""
    full_path = f"{file_directory}/{file_name}"
    os.makedirs(
        os.path.join(os.getcwd(), file_directory),
        exist_ok=True,
    )

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print(f"File written to {full_path}")
