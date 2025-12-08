#!/usr/bin/env python3

import json
from dataclasses import dataclass
from pathlib import Path
from typing import assert_never

import docx
from data_parsing import initialize_database_for_xml
from docx.table import Table, _Row
from docx.text.paragraph import Paragraph
from typing_utils.translations_classes import Database


@dataclass
class ImageEntry:
    image: str
    caption: str


@dataclass
class BiographyEntry:
    sources: str
    olandese: str
    inglese: str
    italiano: str


@dataclass
class FullEntry:
    identifier: str
    image: ImageEntry | None
    biography: BiographyEntry


def _parse_paragraph(paragraph: Paragraph, database: Database) -> str | None:
    # Strip as the file contains empty paragraphs and trailing/leading whitespace
    text = paragraph.text.strip()
    if not text:
        return None

    assert text in database.individuals, f"Identifier '{text}' not found in database"
    return text


def _parse_image_entry(image_row: _Row, caption_row: _Row, images_path: Path) -> ImageEntry | None:
    assert len(image_row.cells) == 2, "Image row must have exactly two cells"
    assert len(caption_row.cells) == 2, "Caption row must have exactly two cells"

    assert image_row.cells[0].text.strip().lower() == "image", (
        "First cell of image row must be 'image'"
    )
    assert caption_row.cells[0].text.strip().lower() == "image caption", (
        "First cell of caption row must be 'image caption'"
    )

    image_link = image_row.cells[1].text.strip()
    caption = caption_row.cells[1].text.strip()

    assert (
        image_link.startswith("$") or image_link.startswith("https://rkd.nl/") or image_link == ""
    )
    if image_link:
        assert caption, "Caption must be provided if image link is present"
    else:
        assert not caption, "Caption must be empty if image link is not present"

    if image_link.startswith("$"):
        for suffix in [".jpg", ".jpeg", ".JPG"]:
            if (images_path / f"{image_link}{suffix}").exists():
                image_link = f"{image_link}{suffix}"
                break
        else:
            raise AssertionError(f"Image file for link '{image_link}' not found")
    return ImageEntry(image=image_link, caption=caption) if image_link else None


def _parse_biography_entry(
    sources: _Row,
    olandese: _Row,
    inglese: _Row,
    italiano: _Row,
) -> BiographyEntry:
    for row in (sources, olandese, inglese, italiano):
        assert len(row.cells) == 2, f"{row.cells[0].text.strip()} row must have exactly two cells"

    assert sources.cells[0].text.strip().lower() == "sources"
    assert olandese.cells[0].text.strip().lower() == "olandese"
    assert inglese.cells[0].text.strip().lower() == "inglese"
    assert italiano.cells[0].text.strip().lower() == "italiano"

    sources_value = sources.cells[1].text.strip()
    olandese_value = olandese.cells[1].text.strip()
    inglese_value = inglese.cells[1].text.strip()
    italiano_value = italiano.cells[1].text.strip()

    assert sources_value and olandese_value and inglese_value and italiano_value

    return BiographyEntry(
        sources=sources_value,
        olandese=olandese_value,
        inglese=inglese_value,
        italiano=italiano_value,
    )


def _parse_table(table: Table, identifier: str, images_path: Path) -> FullEntry | None:
    assert len(table.rows) == 6

    return FullEntry(
        identifier=identifier,
        image=_parse_image_entry(table.rows[0], table.rows[1], images_path),
        biography=_parse_biography_entry(
            table.rows[2], table.rows[3], table.rows[4], table.rows[5]
        ),
    )


def import_biography_from_docx() -> None:
    database = initialize_database_for_xml()

    with open("/Users/daniel/Documents/Downloads/Biographies.docx", "rb") as f:
        document = docx.Document(f)

    current_identifier: str | None = None
    seen_identifiers: set[str] = set()
    identifiers: dict[str, FullEntry] = {}
    images_dir = (
        Path("/Users")
        / "daniel"
        / "Documents"
        / "Downloads"
        / "swisstransfer_05fa3617-1e20-4f5f-848c-6fad5dc4d1dc"
    )

    for i in document.iter_inner_content():
        match i:
            case Paragraph():
                current_identifier = _parse_paragraph(i, database)
                assert current_identifier not in seen_identifiers, (
                    f"Duplicate identifier '{current_identifier}' found"
                )

                if current_identifier:
                    seen_identifiers.add(current_identifier)

            case Table():
                assert current_identifier, "Table found without preceding identifier paragraph"
                assert current_identifier not in identifiers, (
                    f"Duplicate data for identifier '{current_identifier}'"
                )

                identifiers[current_identifier] = _parse_table(i, current_identifier, images_dir)

            case _:
                assert_never(i)

    assert len(identifiers) == len(seen_identifiers), (
        "Mismatch between seen identifiers and parsed data"
    )

    for file in (images_dir).iterdir():
        if file.stem == ".DS_Store":
            continue
        assert identifiers[file.stem] and identifiers[file.stem].image is not None, (
            f"File '{file.name}' has no matching identifier"
        )

    # with open("inputs/Individuals.json", encoding="utf-8") as f:
    #     individuals = json.load(f)

    # for id_ in individuals:
    #     if id_ == "$schema":
    #         continue

    #     individuals[id_]["image_caption"] = None
    #     individuals[id_]["image_filename"] = None
    #     del individuals[id_]["images"]
    #     del individuals[id_]["biography_sources"]

    # for id_, entry in identifiers.items():
    #     individuals[id_]["sources"] = sorted(entry.biography.sources.split("\n"))
    #     if entry.image:
    #         individuals[id_]["image_caption"] = entry.image.caption
    #         individuals[id_]["image_filename"] = entry.image.image

    # with open("inputs/Individuals.json", "w", encoding="utf-8") as f:
    #     json.dump(individuals, f, ensure_ascii=False, indent=4)


def import_images_from_docx() -> None:
    database = initialize_database_for_xml()

    with open("/Users/daniel/Documents/Downloads/Images.docx", "rb") as f:
        document = docx.Document(f)

    identifiers: dict[str, ImageEntry] = {}
    images_dir = (
        Path("/Users")
        / "daniel"
        / "Documents"
        / "Downloads"
        / "swisstransfer_b41edb04-959c-4a88-98d4-3c76a0bf4642"
    )

    for i in document.iter_inner_content():
        match i:
            case Paragraph():
                assert not i.text.strip(), "Empty paragraph found"

            case Table():
                identifier = i.rows[0].cells[1].text.strip()
                entry = _parse_image_entry(i.rows[0], i.rows[1], images_dir)
                assert entry is not None, "Image entry must not be None"
                assert identifier not in identifiers, "Duplicate image identifier found"
                assert identifier in database.individuals, (
                    f"Image identifier '{identifier}' not found in database"
                )
                identifiers[identifier] = entry

            case _:
                assert_never(i)

    for file in (images_dir).iterdir():
        if file.stem == ".DS_Store":
            continue
        assert identifiers[file.stem] and identifiers[file.stem].image is not None, (
            f"File '{file.name}' has no matching identifier"
        )

    with open("inputs/Individuals.json", encoding="utf-8") as f:
        individuals = json.load(f)

    for id_, entry in identifiers.items():
        individuals[id_]["image_caption"] = entry.caption
        individuals[id_]["image_filename"] = entry.image

    with open("inputs/Individuals.json", "w", encoding="utf-8") as f:
        json.dump(individuals, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import_biography_from_docx()
    import_images_from_docx()
