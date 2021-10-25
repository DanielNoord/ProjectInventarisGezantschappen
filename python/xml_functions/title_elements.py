import re
from typing import Literal, Optional

from data_parsing import control_title, name_string
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


def fix_quotes(title: str) -> str:
    """Change the double quotes in a title to be “ or ” based on occurence"""
    for occurence, quote_match in enumerate(re.finditer(r"\"|“|”", title)):
        if occurence % 2:
            quote = "”"
        else:
            quote = "“"
        pos = quote_match.start()
        title = "".join((title[:pos], quote, title[pos + 1 :]))
    return title


def add_italics(parent_element: etree._Element, title: str) -> None:
    """Appends the title to the parent_element and inserts emph elements if necessary"""
    if "_" in title:
        if not title.count("_") // 2:
            raise ValueError(f"Unbalanced amount of italics indicators '_' in {title}")

        title_split = title.split("_")

        parent_element.text = title_split[0]

        # Insert a emph element for every odd index, skipping zero
        for index, string in enumerate(title_split[1:-1]):
            if not index // 2:
                emph = etree.Element("emph", {"render": "italic"})
                emph.text = string
                emph.tail = title_split[index + 2]
                parent_element.append(emph)
    else:
        parent_element.text = title


def add_unittitle(
    parent_element: etree._Element, title: str, database: Database, date: str
) -> Optional[re.Pattern[str]]:
    """Adds a unittitle to the parent element"""
    title_en, title_nl, title_it = title, title, title
    used_trans = None

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
            used_trans = pattern

    title_it = fill_in_name(title_it, database, date, "it_IT")
    title_en = fill_in_name(title_en, database, date, "en_GB")
    title_nl = fill_in_name(title_nl, database, date, "nl_NL")

    # Add and check italics
    if sum("_" in i for i in (title_it, title_en, title_nl)) == 1:
        raise ValueError(
            f"Italics indication is not the same for English and Dutch translation of {title}"
        )

    if re.match(r"\"|“|”", title_it):
        title_it = fix_quotes(title_it)
        title_en = fix_quotes(title_en)
        title_nl = fix_quotes(title_nl)

    control_title(title_it, parent_element)
    control_title(title_en, parent_element)
    control_title(title_nl, parent_element)

    add_italics(etree.SubElement(parent_element, "unittitle", {"lang": "it"}), title_it)
    add_italics(etree.SubElement(parent_element, "unittitle", {"lang": "en"}), title_en)
    add_italics(
        etree.SubElement(parent_element, "unittitle", {"lang": "dut"}), title_nl
    )

    return used_trans
