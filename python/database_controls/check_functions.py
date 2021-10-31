from date_functions import extract_date
from typing_utils import IndividualsDictEntry, TranslationDictCleaned


def control_functions(
    data: IndividualsDictEntry,
    translated_functions: TranslationDictCleaned,
    identifier: str,
    used_functions: set[str],
) -> None:
    """Controls functions of the supplied data

    Args:
        data: Data dict of identifier
        translated_functions: Dict with titles currently translated
        identifier: Identifier of person with titles
        used_functions: List to track titles in use in database

    Raises:
        KeyError: When function is not found in current translations
        ValueError: When the function entry does not have 2 elements but too little
        ValueError: When the function entry does not have 2 elements but too many
        ValueError: When the timeperiod does not have a correct (1-12) month
        ValueError: Unrecognized ValueError's
    """
    try:
        for function, timeperiod in data["functions"]:
            try:
                assert translated_functions[function]
            except KeyError as err:
                raise KeyError(
                    f"Don't recgonize '{function}' from {identifier}. "
                    "Has it been added to inputs/Translations/Functions.json?"
                ) from err
            if timeperiod is not None:
                assert extract_date(timeperiod, "nl_NL")
            used_functions.add(function)
    except ValueError as err:
        if err.args[0] == "not enough values to unpack (expected 2, got 1)":
            raise ValueError(
                f"One of the functions of {identifier} does not follow standard pattern.\n"
                "Perhaps you need to split the date and function? Or is not empty correctly?"
            ) from err
        if err.args[0] == "too many values to unpack (expected 2)":
            raise ValueError(
                f"One of the functions of {identifier} does not follow standard pattern.\n"
                "There are too many strings"
            ) from err
        if err.args[0] == "month must be in 1..12":
            raise ValueError(
                f"{timeperiod} of '{function}' of {identifier} does not follow standard pattern.\n"
                "The month is not between 1 or 12 or you're not using a '/' correctly"
            ) from err
        print(err.args[0])
        if err.args[0].startswith("The first date"):
            raise ValueError(f"{err.args[0]} for '{function}' of {identifier}") from err
        raise ValueError(
            f"Unrecognized error. Please check the functions of {identifier} again"
        ) from err
