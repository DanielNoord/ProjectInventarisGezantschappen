import re
from typing import List, Literal, Optional

from data_parsing import full_name_with_database
from date_functions import check_date
from lxml import etree
from typing_utils import Database, IndividualsDictEntry


def name_string(
    person: IndividualsDictEntry,
    date: str,
    database: Database,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> str:
    """Creates a string of a given person"""
    date_list: List[Optional[int]] = [int(i) if i else None for i in date.split("-")]
    while len(date_list) != 3:
        date_list.append(None)
    date_tuple = (date_list[0], date_list[1], date_list[2])

    # Create Full Name variable
    str_full_name = full_name_with_database(
        person["surname"],
        person["name"],
        person["titles"],
        database,
        localization,
        date_tuple,
    )

    # Create Full Name + function variable
    if person["functions"] != []:
        relevant_functions = []
        for func in person["functions"]:
            if func:
                if func[1] is None or date_tuple[0] is None:
                    relevant_functions.append(func)
                elif check_date(date_tuple, func[1]):
                    relevant_functions.append(func)
        if localization != "it_IT":
            str_functions = ", ".join(
                [database.functions[i[0]][localization] for i in relevant_functions]
            )
        else:
            str_functions = ", ".join([i[0] for i in relevant_functions])
        if str_functions != "":
            return f"{str_full_name} ({str_functions})"
    return str_full_name


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
