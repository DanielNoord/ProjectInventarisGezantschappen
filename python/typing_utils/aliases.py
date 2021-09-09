from typing import TypedDict, Union

TranslationDictEntry = TypedDict("TranslationDictEntry", {"nl_NL": str, "en_GB": str})
TranslationDict = dict[str, Union[str, TranslationDictEntry]]
TranslationDictCleaned = dict[str, TranslationDictEntry]
TranslationDictEntryTitles = TypedDict(
    "TranslationDictEntryTitles", {"nl_NL": str, "en_GB": str, "position": str}
)
TranslationDictTitles = dict[str, Union[str, TranslationDictEntryTitles]]
TranslationDictCleanedTitles = dict[str, TranslationDictEntryTitles]
