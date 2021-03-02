import re


def person(input_line):
    """Parses a person string
    
    Args:
        input_line (str): Line to be parsed

    Returns:
        str: Identifier
        str: Surname
        str: Name
        str: Nationality
        str: Title
        str: Function
        str: Place of residence
    """
    pattern = re.compile(r"- (.*); (.*); (.*); (.*); (.*); (.*); (.*);;", re.DOTALL)
    return re.match(pattern, input_line).groups()
