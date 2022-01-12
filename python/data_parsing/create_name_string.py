from typing import Literal, Union

from date_functions import check_date, create_date_tuple
from typing_utils import Database, DateTuple, IndividualsDictEntry

from data_parsing.create_full_name_string import full_name_with_database


def name_string(
    person: IndividualsDictEntry,
    date: Union[str, DateTuple],
    database: Database,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> str:
    """Creates a string of a given person"""
    date_tuple = create_date_tuple(date)

    # Create Full Name variable
    str_full_name = full_name_with_database(
        person["surname"],
        person["name"],
        person["titles"],
        database,
        localization,
        date_tuple,
    )

    # Create Full Name + function variable
    if person["functions"] != []:
        relevant_functions = []
        for func in person["functions"]:
            if func:
                if func[1] is None or date_tuple[0] is None:
                    relevant_functions.append(func)
                elif check_date(date_tuple, func[1]):
                    relevant_functions.append(func)
        if localization != "it_IT":
            str_functions = ", ".join(
                [database.functions[i[0]][localization] for i in relevant_functions]
            )
        else:
            str_functions = ", ".join([i[0] for i in relevant_functions])
        if str_functions != "":
            str_full_name = f"{str_full_name} ({str_functions})"
    return str_full_name.replace("{", "(").replace("}", ")")
