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

    if titles[0] != "":
        translation_entry = translation_data[0][titles[0]]
        if translation_entry["position"] == "Before":
            if name == "":
                str_full_name = f"{translation_entry[localization]} {surname}"
            else:
                str_full_name = f"{translation_entry[localization]} {name} {surname}"
        elif translation_entry["position"] == "After":
            str_full_name = f"{surname}, {translation_entry[localization]},"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        elif translation_entry["position"] == "Middle":
            str_full_name = f"{translation_entry[localization]} {surname}"
            if name != "":
                str_full_name = f"{name} {str_full_name}"
        else:
            raise Exception(f"Don't recognize type of {titles[0]}")

        if len(titles) > 1:
            for extra_title in titles[1:]:
                translation_entry = translation_data[0][extra_title]
                if translation_entry["position"] == "Before":
                    str_full_name = f"{translation_entry[localization]} {str_full_name}"
                elif translation_entry["position"] == "After":
                    str_full_name += f" {translation_entry[localization]},"
                else:
                    raise Exception("Can't parse second title, maybe change order in sourcefile")
    else:
        if name != "":
            str_full_name = f"{name} {surname}"
        else:
            str_full_name = surname
    return str_full_name
