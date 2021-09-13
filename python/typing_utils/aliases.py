from typing import Optional, Pattern, TypedDict, Union

# Dictionaries for the Translation files
TranslationDictEntry = TypedDict("TranslationDictEntry", {"nl_NL": str, "en_GB": str})
TranslationDict = dict[str, Union[str, TranslationDictEntry]]
TranslationDictCleaned = dict[str, TranslationDictEntry]
TranslationDictCleanedDocuments = dict[Pattern[str], TranslationDictEntry]
TranslationDictEntryTitles = TypedDict(
    "TranslationDictEntryTitles", {"nl_NL": str, "en_GB": str, "position": str}
)
TranslationDictTitles = dict[str, Union[str, TranslationDictEntryTitles]]
TranslationDictCleanedTitles = dict[str, TranslationDictEntryTitles]

# Dictionaries for the Individuals file
IndividualsDictEntry = TypedDict(
    "IndividualsDictEntry",
    {
        "surname": str,
        "person_type": int,
        "name": str,
        "date_of_birth": str,
        "place_of_birth": str,
        "date_of_death": str,
        "place_of_death": str,
        "titles": list[tuple[str, Optional[str]]],
        "functions": list[tuple[str, Optional[str]]],
        "comment": str,
        "comment_daniel": str,
        "sources": list[str],
        "images": list[str],
    },
)
IndividualsDict = dict[str, Union[str, IndividualsDictEntry]]
IndividualsDictCleaned = dict[str, IndividualsDictEntry]
