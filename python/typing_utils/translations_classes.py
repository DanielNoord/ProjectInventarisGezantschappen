from typing import Dict, NamedTuple, Optional, Pattern, TypedDict, Union


# Dictionaries for the Translation files
class TranslationDictEntry(TypedDict):
    nl_NL: str
    en_GB: str


class TranslationDictEntryTitles(TypedDict):
    nl_NL: str
    en_GB: str
    position: str


class TranslationDictEntryPlacenames(TypedDict):
    nl_NL: str
    en_GB: str
    geonames_id: int
    geonames_wikipedia: str
    longitude: str
    latitude: str


TranslationDict = Dict[str, Union[str, TranslationDictEntry]]
TranslationDictCleaned = Dict[str, TranslationDictEntry]

TranslationDictCleanedDocuments = Dict[Pattern[str], TranslationDictEntry]

TranslationDictTitles = Dict[str, Union[str, TranslationDictEntryTitles]]
TranslationDictCleanedTitles = Dict[str, TranslationDictEntryTitles]

TranslationDictPlacenames = Dict[str, Union[str, TranslationDictEntryPlacenames]]
TranslationDictCleanedPlacenames = Dict[str, TranslationDictEntryPlacenames]

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
        "wikidata:id": Optional[str],
        "ISNI:id": Optional[str],
    },
)
IndividualsDict = Dict[str, Union[str, IndividualsDictEntry]]
IndividualsDictCleaned = Dict[str, IndividualsDictEntry]


class Database(NamedTuple):
    """A fully loaded database of all data collected in the project."""

    document_titles: TranslationDictCleanedDocuments
    functions: TranslationDictCleaned
    placenames: TranslationDictCleanedPlacenames
    titles: TranslationDictCleanedTitles
    individuals: IndividualsDictCleaned
