import create_docx
import parse_docx
import read_docx

def generate_person_list(filename):
    print("Extracting names and writing file")
    persons_in_file = read_docx.extract_persons(filename)
    list_of_parsed_persons = []

    used_functions = []
    for person in persons_in_file:
        surname, name, nationality, titles, function, place_of_residence = parse_docx.person(person)

        # Create Full Name variable
        str_full_name = parse_docx.create_full_name(surname, name, titles)

        # Parse functions
        if function != "":
            functions = parse_docx.function(function)
            str_functions = ", ".join([i[0] for i in functions])
            for i in functions:
                used_functions.append(i[0])

        # Create Full Name + function variable
        str_full_name_function = str_full_name
        if function:
            str_full_name_function = f"{str_full_name} ({str_functions})"

        list_of_parsed_persons.append(str_full_name_function)
        #print(str_full_name_function)

    create_docx.write_list(list_of_parsed_persons, "outputs/Namenlijst.docx")
    create_docx.write_list(sorted(list(set(used_functions))), "outputs/Functielijst.docx")

    print("Extraction and writing complete!")

if __name__ == "__main__":
    generate_person_list("inputs/Eigennamen.docx")
