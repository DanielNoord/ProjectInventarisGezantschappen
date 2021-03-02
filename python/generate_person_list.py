from read_docx.extract_persons import extract_persons
from translate.translate import initliaze_translation_database
from docx_to_names.parse_person import  parse_person

def generate_person_list(input_file, language = "All"):
    persons_in_file = extract_persons(input_file)
    translation_data = initliaze_translation_database()

    # Output lists
    all_parsed_persons = []
    all_functions = []
    all_titles = []
    all_full_names = []
    data_with_identifier = {}

    for person in persons_in_file:
        if person[2] != "$":
            raise Exception(f"No identifier found for ${person}")

        # Create data from persons
        if language in ("all", "nl_NL"):
            full_name_function_nl_nl, full_name_nl_nl,\
                identifier, functions, titles = parse_person("nl_NL", person, translation_data)
        if language in ("all", "it_IT"):
            full_name_function_it_it, _, _, _, _ = parse_person("it_IT", person, translation_data)
        if language in ("all", "en_GB"):
            full_name_function_en_gb, _, _, _, _ = parse_person("en_GB", person, translation_data)

        if identifier in data_with_identifier.keys():
            raise Exception(f"Identifier of {full_name_nl_nl} is a duplicate")

        # Populate data to be exported
        for i in functions:
            all_functions.append(i[0])
        for i in titles.split("| "):
            all_titles.append(i)
        all_parsed_persons.append(full_name_function_nl_nl)
        all_full_names.append(full_name_function_nl_nl)
        if language == "all":
            data_with_identifier[identifier] = {
                "it_IT": full_name_function_it_it,
                "nl_NL": full_name_function_nl_nl,
                "en_GB": full_name_function_en_gb,
                }

        print(full_name_nl_nl)

    return data_with_identifier, all_parsed_persons,\
        all_full_names, sorted(list(set(all_functions))), sorted(list(set(all_titles)))
