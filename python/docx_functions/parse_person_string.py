import re
from typing import Sequence


def parse_person(input_line: str) -> Sequence[str]:
    """Parses a person string

    Args:
        input_line: Line to be parsed

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
    if (mat := re.match(pattern, input_line)) and len(mat.groups()) == 10:
        return mat.groups()
    raise ValueError(f"Can't parse the following person string:\n{input_line}")
