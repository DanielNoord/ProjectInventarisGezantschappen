from __future__ import annotations

from re import Pattern
from typing import NamedTuple, TypedDict


# Dictionaries for the Translation files
class TranslationDictEntry(TypedDict):
    """Simple translation entry."""

    nl_NL: str
    en_GB: str


class TranslationDictEntryTitles(TypedDict):
    """Title translation entry."""

    nl_NL: str
    en_GB: str
    position: str


class TranslationDictEntryPlacenames(TypedDict):
    """Placename translation entry."""

    nl_NL: str
    en_GB: str
    geonames_id: int
    geonames_wikipedia: str | None
    longitude: str
    latitude: str


TranslationDict = dict[str, str | TranslationDictEntry]
TranslationDictCleaned = dict[str, TranslationDictEntry]

TranslationDictCleanedDocuments = dict[Pattern[str], TranslationDictEntry]

TranslationDictTitles = dict[str, str | TranslationDictEntryTitles]
TranslationDictCleanedTitles = dict[str, TranslationDictEntryTitles]

TranslationDictPlacenames = dict[str, str | TranslationDictEntryPlacenames]
TranslationDictCleanedPlacenames = dict[str, TranslationDictEntryPlacenames]

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
        "titles": list[tuple[str, str | None]],
        "functions": list[tuple[str, str | None]],
        "comment": str,
        "comment_daniel": str,
        "sources": list[str],
        "images": list[str],
        "wikidata:id": str | None,
        "ISNI:id": str | None,
    },
)
IndividualsDict = dict[str, str | IndividualsDictEntry]
IndividualsDictCleaned = dict[str, IndividualsDictEntry]


class Database(NamedTuple):
    """A fully loaded database of all data collected in the project."""

    document_titles: TranslationDictCleanedDocuments
    functions: TranslationDictCleaned
    placenames: TranslationDictCleanedPlacenames
    titles: TranslationDictCleanedTitles
    individuals: IndividualsDictCleaned
