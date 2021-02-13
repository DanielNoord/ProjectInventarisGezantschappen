import create_docx
import parse_docx
import read_docx

def generate_person_list(filename):
    print("Extracting names and writing file")
    persons_in_file = read_docx.extract_persons(filename)
    list_of_parsed_persons = []

    for person in persons_in_file:
        surname, name, nationality, title, function, place_of_residence = parse_docx.person(person)

        # Create Full Name variable
        if surname == "":
            raise Exception(f"{person} has no surname!")
        str_full_name = surname
        if name != "":
            str_full_name = f"{name} {surname}"

        # Parse functions
        if function != "":
            functions = parse_docx.function(function)
            str_functions = ", ".join([i[0] for i in functions])

        # Create Full Name + function variable
        str_full_name_function = str_full_name
        if function:
            str_full_name_function = f"{str_full_name} ({str_functions})"

        list_of_parsed_persons.append(str_full_name_function)
        # print(str_full_name_function)

    create_docx.write_list(list_of_parsed_persons)

    print("Extraction and writing complete!")

if __name__ == "__main__":
    generate_person_list("Eigennamen.docx")
