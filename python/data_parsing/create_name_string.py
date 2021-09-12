#!/usr/bin/env python3

from typing import Literal, Optional

from date_functions import check_date
from typing_utils import (
    TranslationDictCleaned,
    TranslationDictCleanedTitles,
    IndividualsDictEntry,
)

from data_parsing import full_name


def name_string(
    person: IndividualsDictEntry,
    date: tuple[Optional[int], Optional[int], Optional[int]],
    translation_data: tuple[
        TranslationDictCleanedTitles, TranslationDictCleaned, TranslationDictCleaned
    ],
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> str:
    """Creates a string of a given person

    Args:
        person (dict): Dictionary of data for the relevant person
        date (tuple[Optional[int], Optional[int], Optional[int]]): Date of the file
        translation_data: Dictionaries with translation data for titles, functions and places
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation

    Returns:
        str: The string of the person as "name (functions)"
    """
    # Create Full Name variable
    str_full_name = full_name(
        person["surname"],
        person["name"],
        person["titles"],
        translation_data,
        localization,
        date,
    )

    # Create Full Name + function variable
    if person["functions"] != []:
        relevant_functions = []
        for func in person["functions"]:
            if func:
                if func[1] is None or date[0] is None:
                    relevant_functions.append(func)
                elif check_date(date, func[1]):
                    relevant_functions.append(func)
        if localization != "it_IT":
            str_functions = ", ".join(
                [translation_data[1][i[0]][localization] for i in relevant_functions]
            )
        else:
            str_functions = ", ".join([i[0] for i in relevant_functions])
        if str_functions != "":
            return f"{str_full_name} ({str_functions})"
    return str_full_name
