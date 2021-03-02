from helper_functions.parse_person import person as read_person
from helper_functions.parse_function import function as read_function
from helper_functions.create_full_name import full_name as create_full_name

def parse_person(localization, person, translation_data):
    identifier, surname, name, _, titles,\
        function, _ = read_person(person)

    # Create Full Name variable
    str_full_name = create_full_name(surname, name, titles, translation_data, localization)

    # Parse functions
    functions = []
    if function != "":
        functions = read_function(function)
        # TODO: Add call look up in translation_data
        str_functions = ", ".join([i[0] for i in functions])

    # Create Full Name + function variable
    str_full_name_function = str_full_name
    if function:
        str_full_name_function = f"{str_full_name} ({str_functions})"

    return str_full_name_function, str_full_name, identifier, functions, titles
