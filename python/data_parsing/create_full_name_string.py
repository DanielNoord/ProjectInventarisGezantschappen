from typing import Literal, Optional, Union

from date_functions import check_date
from typing_utils import Database, DateTuple


def full_name_with_database(  # pylint: disable=too-many-arguments, too-many-branches
    surname: str,
    name: str,
    titles: list[tuple[str, Optional[str]]],
    database: Database,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
    date: Union[tuple[DateTuple], tuple[DateTuple, DateTuple]],
) -> str:
    """Creates the string for the full name including any possible titles"""
    if surname == "":
        raise Exception(f"{name} has no surname!")

    relevant_titles = []
    for title in titles:
        if title:
            if title[1] is None or date[0] is None:
                relevant_titles.append(title)
            elif check_date(date, title[1]):
                relevant_titles.append(title)
    if relevant_titles:
        translation_entry = database.titles[relevant_titles[0][0]]
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
                translation_entry = database.titles[extra_title[0]]
                if localization != "it_IT":
                    translated_title = translation_entry[localization]
                else:
                    translated_title = relevant_titles[0][0]
                if translation_entry["position"] == "Before":
                    str_full_name = f"{translated_title} {str_full_name}"
                elif translation_entry["position"] == "After":
                    str_full_name += f" {translated_title},"
                else:
                    raise Exception(
                        "Can't parse second title, maybe change order in sourcefile"
                    )
    else:
        if name != "":
            str_full_name = f"{name} {surname}"
        else:
            str_full_name = surname
    return str_full_name
