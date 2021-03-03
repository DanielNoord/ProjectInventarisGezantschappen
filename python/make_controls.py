from functions.create_docx import list_of_translated_data
from functions.translate import initialize_translation_database


def create_controle_transaltions():
    """Create .docx files of all titles and functions found by the translate functions
    Includes Italian and English translations on second and third row
    """
    data = initialize_translation_database()

    translated_titles = []
    translated_functions = []

    for title, translations in sorted(data[0].items()):
        result = [title]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        translated_titles.append(result)

    for function, translations in sorted(data[1].items()):
        result = [function]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        translated_functions.append(result)

    list_of_translated_data(translated_titles, "Titles")
    list_of_translated_data(translated_functions, "Functions")


if __name__ == "__main__":
    create_controle_transaltions()
