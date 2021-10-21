#!/usr/bin/env python3
# type: ignore # pylint: disable-all

from functions.helper_functions.create_full_name import full_name as create_full_name


def create_person(
    localization: Literal["it_IT", "nl_NL", "en_GB"],
    person: dict,
    translation_data: list[dict, dict, dict],
) -> tuple[str, str]:
    """Creates a data entry for the given person

    Args:
        localization (Literal["it_IT", "nl_NL", "en_GB"]): Localization abbreviation
        person (dict): The data of the person in dictionary formt
        translation_data: Dictionaries with translation data for titles, functions and places

    Returns:
        str: Full name and function
        str: Full name
    """
    # Create Full Name variable
    str_full_name = create_full_name(
        person["surname"],
        person["name"],
        person["titles"],
        translation_data,
        localization,
        [None],
    )

    # Create Full Name + function variable
    str_full_name_function = str_full_name
    if person["functions"] != [""]:
        str_functions = ", ".join(
            [translation_data[1][i[0]][localization] for i in person["functions"]]
        )
        if str_functions != "":
            str_full_name_function = f"{str_full_name} ({str_functions})"

    return str_full_name_function, str_full_name
