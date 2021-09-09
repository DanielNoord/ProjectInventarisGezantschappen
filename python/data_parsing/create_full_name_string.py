#!/usr/bin/env python3

from date_functions import check_date


def full_name(  # pylint: disable=too-many-arguments, too-many-branches
    surname: str,
    name: str,
    titles: str,
    translation_data: tuple[dict, dict, dict],
    localization: str,
    date: list[int],
) -> str:
    """Creates the string for the full name including title

    Args:
        surname (str): Surname of individual
        name (str): First name of indiviudal
        titles (str): Function of indiviudal
        translation_data: Dictionaries with translation data for titles, functions and places
        localization (str): Localization to be used ("nl_NL", "it_IT" or "en_GB")
        date (list[int]): Date of the file to be checked

    Raises:
        Exception: When there is no surname
        Exception: When a title is not recognized
        Exception: When a second title can not be fitted

    Returns:
        str: The full title of the given individual
    """
    if surname == "":
        raise Exception(f"{name} has no surname!")

    relevant_titles = []
    for title in titles:
        if title[1] is None or date[0] is None:
            relevant_titles.append(title)
        elif check_date(date, title[1]):
            relevant_titles.append(title)
    if relevant_titles != []:
        translation_entry = translation_data[0][relevant_titles[0][0]]
        if localization != "it_IT":
            translated_title = translation_entry[localization]
        else:
            translated_title = relevant_titles[0][0]
        if translation_entry["position"] == "Before":
            if name == "":
                str_full_name = f"{translated_title} {surname}"
            else:
                str_full_name = f"{translated_title} {name} {surname}"
        elif translation_entry["position"] == "After":
            str_full_name = f"{surname}, {translated_title},"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        elif translation_entry["position"] == "Middle":
            str_full_name = f"{translated_title} {surname}"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        else:
            raise Exception(f"Don't recognize type of {relevant_titles[0][0]}")

        if len(relevant_titles) > 1:
            for extra_title in relevant_titles[1:]:
                translation_entry = translation_data[0][extra_title[0]]
                if localization != "it_IT":
                    translated_title = translation_entry[localization]
                else:
                    translated_title = relevant_titles[0][0]
                if translation_entry["position"] == "Before":
                    str_full_name = f"{translated_title} {str_full_name}"
                elif translation_entry["position"] == "After":
                    str_full_name += f" {translated_title},"
                else:
                    raise Exception("Can't parse second title, maybe change order in sourcefile")
    else:
        if name != "":
            str_full_name = f"{name} {surname}"
        else:
            str_full_name = surname
    return str_full_name
