from create_docx.write_list_translated_names import write_list_translated_names
from translate.translate import initliaze_translation_database


def create_controle_transaltions():
    """Create .docx files of all titles and functions found by the translate functions
    Includes Italian and English translations on second and third row
    """
    data = initliaze_translation_database()

    translated_titles = []
    translated_functions = []

    for title, translations in data[0].items():
        result = [title]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        translated_titles.append(result)

    for function, translations in data[1].items():
        result = [function]
        result.append(translations["it_IT"])
        result.append(translations["en_GB"])
        translated_functions.append(result)

    write_list_translated_names(translated_titles, "Titles")
    write_list_translated_names(translated_functions, "Functions")

if __name__ == "__main__":
    create_controle_transaltions()
