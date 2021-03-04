import re


def person(input_line):
    """Parses a person string

    Args:
        input_line (str): Line to be parsed

    Returns:
        str: Identifier
        str: Person type
        str: Surname
        str: Name
        str: Nationality
        str: Title
        str: Function
        str: Place of residence
        str: Comment
        str: Sources
    """
    pattern = re.compile(
        r"- (.*); (.*); (.*); (.*); (.*); (.*); (.*); (.*); (.*); (.*);;", re.DOTALL
    )
    return re.match(pattern, input_line).groups()
