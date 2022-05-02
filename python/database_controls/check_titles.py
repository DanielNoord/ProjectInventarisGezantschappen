from date_functions import extract_date
from typing_utils import IndividualsDictEntry, TranslationDictCleanedTitles


def control_titles(
    data: IndividualsDictEntry,
    translated_titles: TranslationDictCleanedTitles,
    identifier: str,
    used_titles: set[str],
) -> None:
    """Controls titles of the supplied data.

    Args:
        data: Data dict of identifier
        translated_titles: Dict with titles currently translated
        identifier: Identifier of person with titles
        used_titles: List to track titles in use in database

    Raises:
        KeyError: When title is not found in current translations
        ValueError: When the title entry does not have 2 elements but too little
        ValueError: When the title entry does not have 2 elements but too many
        ValueError: When the timeperiod does not have a correct (1-12) month
        ValueError: Unrecognized ValueError's
    """
    try:
        for title, timeperiod in data["titles"]:
            try:
                assert translated_titles[title]
            except KeyError as err:
                raise KeyError(
                    f"Don't recgonize '{title}' from {identifier}. "
                    "Has it been added to inputs/Translations/Titles.json?"
                ) from err
            if timeperiod is not None:
                assert extract_date(timeperiod, "nl_NL")
            used_titles.add(title)
    except ValueError as err:
        if err.args[0] == "not enough values to unpack (expected 2, got 1)":
            raise ValueError(
                f"One of the titles of {identifier} does not follow standard pattern.\n"
                "Perhaps you need to split the date and title? Or is not empty correctly?"
            ) from err
        if err.args[0] == "too many values to unpack (expected 2)":
            raise ValueError(
                f"One of the titles of {identifier} does not follow standard pattern.\n"
                "There are too many strings"
            ) from err
        if err.args[0] == "month must be in 1..12":
            raise ValueError(
                f"{timeperiod} of '{title}' of {identifier} does not follow standard pattern.\n"
                "The month is not between 1 or 12 or you're not using a '/' correctly"
            ) from err
        if err.args[0].startswith("The first date"):
            raise ValueError(f"{err.args[0]} for '{title}' of {identifier}") from err
        print(err.args[0])
        raise ValueError(
            f"Unrecognized error. Please check the titles of {identifier} again"
        ) from err
