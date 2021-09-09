#!/usr/bin/env python3

from typing import Union

from date_functions import check_date

from data_parsing import full_name


def name_string(
    person: dict,
    date: list[Union[int, None]],
    translation_data: list[dict, dict, dict],
    localization: str,
) -> str:
    """Creates a string of a given person

    Args:
        person (dict): Dictionary of data for the relevant person
        date (list[Union[int, None]]): Date of the file in which the person is mentioned
        translation_data (list[dict, dict, dict]): Dictionaries of functions and title translations
        localization (str): Localization abbreviation ("nl_NL", "it_IT", "en_GB")

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
