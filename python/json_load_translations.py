import json
import os
import re

import docx


def load_translations_documents(filename):
    """Load translations from .docx and write .json for documents file

    Args:
        filename (str): Filename of the input file
    """
    doc = docx.Document(filename)
    all_placenames = {"$schema": "../../static/JSON/DocumentTitles.json"}

    for para in doc.paragraphs:
        (it_it_trans, nl_nl_trans, en_gb_trans) = re.split(r"\n.*?", para.text)

        all_placenames[it_it_trans] = {"en_GB": en_gb_trans, "nl_NL": nl_nl_trans}

    with open("outputs/DocumentTitles.json", "w", encoding="utf-8") as file:
        json.dump(all_placenames, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print("Wrote file to outputs/DocumentTitles.json")


def load_translations_functions(filename):
    """Load translations from .docx and write .json for functions file

    Args:
        filename (str): Filename of the input file
    """
    doc = docx.Document(filename)
    all_placenames = {"$schema": "../../static/JSON/Functions.json"}

    for para in doc.paragraphs:
        (nl_nl_trans, it_it_trans, en_gb_trans) = re.split(r"\n.*?", para.text)

        all_placenames[nl_nl_trans] = {
            "en_GB": en_gb_trans,
            "it_IT": it_it_trans,
            "nl_NL": nl_nl_trans,
        }

    with open("outputs/Functions.json", "w", encoding="utf-8") as file:
        json.dump(all_placenames, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print("Wrote file to outputs/Functions.json")


def load_translations_placenames(filename):
    """Load translations from .docx and write .json for placename file

    Args:
        filename (str): Filename of the input file
    """
    doc = docx.Document(filename)
    all_placenames = {"$schema": "../../static/JSON/Placenames.json"}

    for para in doc.paragraphs:
        (it_it_trans, nl_nl_trans, en_gb_trans) = re.split(r"\n.*?", para.text)

        all_placenames[it_it_trans] = {"en_GB": en_gb_trans, "nl_NL": nl_nl_trans}

    with open("outputs/Placenames.json", "w", encoding="utf-8") as file:
        json.dump(all_placenames, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print("Wrote file to outputs/Placenames.json")


def load_translations_titles(filename):
    """Load translations from .docx and write .json for titles file

    Args:
        filename (str): Filename of the input file
    """
    doc = docx.Document(filename)
    all_placenames = {"$schema": "../../static/JSON/Titles.json"}

    for para in doc.paragraphs:
        (nl_nl_trans, it_it_trans, en_gb_trans, position) = re.split(r"\n.*?", para.text)

        all_placenames[nl_nl_trans] = {
            "en_GB": en_gb_trans,
            "it_IT": it_it_trans,
            "nl_NL": nl_nl_trans,
            "position": position.replace("position: ", ""),
        }

    with open("outputs/Titles.json", "w", encoding="utf-8") as file:
        json.dump(all_placenames, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print("Wrote file to outputs/Titles.json")


if __name__ == "__main__":
    dname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(dname)

    load_translations_documents("inputs/Translations/Controle/TranslatedDocumentTitles.docx")
    # load_translations_functions("inputs/Translations/Controle/TranslatedFunctions.docx")
    # load_translations_placenames("inputs/Translations/Controle/TranslatedPlacenames.docx")
    # load_translations_titles("inputs/Translations/Controle/TranslatedTitles.docx")
