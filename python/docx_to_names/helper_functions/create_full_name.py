import re

ACCEPTED_PRE_TITLES = ["kard.", "mgr.", "mr.", "jhr.", "luitenant-generaal b.d.",
    "luitenant-generaal", "majoor-generaal", "admiraal", "generaal",
    "schout-bij-nacht", "commandant", "luitenant-kolonel", "ridder",
    "Paus"]
ACCEPTED_MIDDLE_TITLES = ["markies", "graaf", "gravin", "baron", "barones", "lord"]
ACCEPTED_FINAL_TITLE = ["markies de .*", "markies van .*", "prins van .*", "prins de .*",
    "baron da .*", "graaf della .*", "graaf de .*", "hertog van .*",
    "commandeur in de Orde .*",
    "4de graaf van Aberdeen", "aartshertog van Oostenrijk", "prins$", "prinses$"]
COMBINED_REGEXS = "(" + ")|(".join(ACCEPTED_FINAL_TITLE) + ")"


def full_name(surname, name, titles, translation_data, localization):
    """ Creates the string for the full name including title

    Args:
        surname (str): Surname of individual
        name (str): First name of indiviudal
        titles (str): Function of indiviudal
        translation_data (list): two dictionaries containing the translation of titles and functions
        locaizaiton (str): Localization to be used ("nl_NL", "it_IT" or "en_GB")

    Raises:
        Exception: When there is no surname
        Exception: When a title is not recognized
        Exception: When a second title can not be fitted

    Returns:
        str: The full title of the given individual
    """
    if surname == "":
        raise Exception(f"{name} has no surname!")
    titles = titles.split("| ")
    if titles[0] != "":
        if titles[0] in ACCEPTED_PRE_TITLES:
            if name == "":
                str_full_name = f"{translation_data[0][titles[0]][localization]} {surname}"
            else:
                str_full_name = f"{translation_data[0][titles[0]][localization]} {name} {surname}"
        elif re.match(COMBINED_REGEXS, titles[0]):
            str_full_name = f"{surname}, {translation_data[0][titles[0]][localization]},"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        elif  titles[0] in ACCEPTED_MIDDLE_TITLES:
            str_full_name = f"{translation_data[0][titles[0]][localization]} {surname}"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        else:
            raise Exception(f"Don't recognize {titles[0]}")
        if len(titles) > 1:
            if titles[1] in ACCEPTED_PRE_TITLES:
                str_full_name = f"{translation_data[0][titles[1]][localization]} {str_full_name}"
            elif re.match(COMBINED_REGEXS, titles[1]):
                str_full_name += f" {translation_data[0][titles[1]][localization]},"
            else:
                raise Exception("Can't parse second title, maybe change order in sourcefile")
    else:
        if name != "":
            str_full_name = f"{name} {surname}"
        else:
            str_full_name = surname
    return str_full_name
