import re
from typing import Literal

from data_parsing import name_string
from lxml import etree
from typing_utils import Database


def fill_in_name(
    title: str,
    database: Database,
    date: str,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> str:
    """Creates a document title with filled in names and functions"""
    title_split = re.split(r"( |\.|,|\(|\))", title)
    for index, word in enumerate(title_split):
        if word.startswith("$"):
            try:
                title_split[index] = name_string(
                    database.individuals[word], date, database, localization
                )
            except KeyError as error:
                raise KeyError(f"Incorrect identifier {error} in {title}") from error
    return "".join(title_split)


def add_doc_title(
    parent_element: etree._Element, title: str, database: Database, date: str
) -> None:
    """Adds a unittitle to the parent element"""
    title_en, title_nl, title_it = title, title, title

    # Find document translation
    for pattern, trans in database.document_titles.items():
        if pattern.match(title):
            try:
                title_en = re.sub(pattern, trans["en_GB"], title)
                title_nl = re.sub(pattern, trans["nl_NL"], title)
            except re.error as error:
                raise re.error(
                    f"At {pattern} found the following error: {error}"
                ) from error

            # TODO: Add this functionality to XML
            # used_translations.add(pattern)
            break

    title_it = fill_in_name(title_it, database, date, "it_IT")
    title_en = fill_in_name(title_en, database, date, "en_GB")
    title_nl = fill_in_name(title_nl, database, date, "nl_NL")

    etree.SubElement(parent_element, "unittitle", {"lang": "it"}).text = title_it
    etree.SubElement(parent_element, "unittitle", {"lang": "en"}).text = title_en
    etree.SubElement(parent_element, "unittitle", {"lang": "dut"}).text = title_nl
