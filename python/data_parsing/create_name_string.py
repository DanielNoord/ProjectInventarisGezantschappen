from typing import List, Literal, Optional, Tuple, Union

from date_functions import check_date
from typing_utils import Database, IndividualsDictEntry

from data_parsing import full_name_with_database


def name_string(
    person: IndividualsDictEntry,
    date: Union[str, Tuple[Optional[int], Optional[int], Optional[int]]],
    database: Database,
    localization: Literal["it_IT", "nl_NL", "en_GB"],
) -> str:
    """Creates a string of a given person"""
    if isinstance(date, str):
        date_list: List[Optional[int]] = [
            int(i) if i else None for i in date.split("-")
        ]
        while len(date_list) != 3:
            date_list.append(None)
        date_tuple = (date_list[0], date_list[1], date_list[2])
    else:
        date_tuple = date

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
            return f"{str_full_name} ({str_functions})"
    return str_full_name
