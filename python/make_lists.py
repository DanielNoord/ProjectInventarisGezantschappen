import docx

from create_docx.write_list import write_list
from create_docx.write_list_to_be_translated import write_list_to_be_translated
from read_docx.extract_persons import extract_persons
from generate_person_list import generate_person_list
from docx_to_names.helper_functions.parse_person import person as parse_person
from docx_to_names.helper_functions.parse_function import function as parse_function

def extract_to_be_translated(input_file):
    persons_in_file = extract_persons(input_file)

    all_functions = []
    all_titles = []
    data_with_identifier = {}

    for person in persons_in_file:
        if person[2] != "$":
            raise Exception(f"No identifier found for ${person}")

        identifier, surname, _, _, titles, function, _ = parse_person(person)

        if identifier in data_with_identifier.keys():
            raise Exception(f"Identifier of {surname} is a duplicate")
        data_with_identifier[identifier]: surname

        functions = []
        if function != "":
            functions = parse_function(function)

        # Populate data to be exported
        for i in functions:
            all_functions.append(i[0])
        for i in titles.split("| "):
            all_titles.append(i)

        print(surname)

    return sorted(list(set(all_functions))), sorted(list(set(all_titles)))

def create_to_be_translated(input_file):
    """ Creates .docx file with all functions and titles to be translated
    Likely unnecessary in future

    Args:
        input_file (str): Name of "database" file with all relevant titles and functions
    """
    functions, titles = extract_to_be_translated(input_file)

    write_list_to_be_translated(functions, "Functions")
    write_list_to_be_translated(titles, "Titles")

def create_names_in_fondo(input_file):
    """ Creates .docx file with all names mentioned in "fondo" file
    Adds a possible identifier for each entry
    Likely unnecessary in future

    Args:
        input_file (str): Name of "fondo" file with all relevant names/entries
    """
    doc = docx.Document(input_file)
    all_text = []
    for para in doc.paragraphs:
        if para.text.startswith("•"):
            all_text.append(para.text[2:])
    all_text = sorted(list(set(all_text)))
    write_list(all_text, "PeopleInFondo.docx")


def create_names(localization, input_file):
    """ Creates a number of .docx files based on "database" file.
    TODO: This function is currently broken

    Args:
        localization (str): Localization of output_files ("nl_NL", "it_IT", "en_GB")
        input_file (str): Name of "database" file
    """
    print("Extracting names and writing file")
    _, parsed_persons, full_names, functions, titles = generate_person_list(input_file)
    write_list(parsed_persons, f"outputs/Volledige Namenlijst_{localization}.docx")
    write_list(full_names, f"outputs/Namenlijst_{localization}.docx")
    write_list(functions, f"outputs/Functielijst_{localization}.docx")
    write_list(titles, f"outputs/Titellijst_{localization}.docx")
    print("Extraction and writing complete!")

if __name__ == "__main__":
    #create_names("nl_NL", "inputs/Eigennamen.docx")
    #create_to_be_translated("inputs/Eigennamen.docx")
    #create_names_in_fondo("inputs/Fondo Legazione Paesi Bassi.docx")
    print("Done!")
