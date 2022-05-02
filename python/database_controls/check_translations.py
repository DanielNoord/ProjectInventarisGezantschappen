from data_parsing import initialize_translation_database


def check_translations() -> None:
    """Checks the JSON files that contain all translations.

    Raises:
        Exception: Whenever there are any duplicates or empty translations
    """
    translated_titles, translated_functions, _ = initialize_translation_database()
    for key, translations_titles in translated_titles.items():
        for translation in translations_titles.values():
            if translation == "":
                raise Exception(f"Found an empty translation in titles at {key}")

    for key, translations in translated_functions.items():
        for translation in translations.values():
            if translation == "":
                raise Exception(f"Found an empty translation in functions at {key}")

    print("Finished checking translations: no missing or broken ones found!\n")
