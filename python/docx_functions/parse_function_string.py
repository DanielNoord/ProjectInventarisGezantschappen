import re


def parse_function(input_line: str) -> list[tuple[str, str | None]]:
    """Parses a function string.

    Args:
        input_line: Line to be parsed

    Returns:
        list[tuple[str, Optional[str]]]: List of tuples
            Each list contains two strings which are title of function and timperiod of function
    """
    pattern = re.compile(r"\w.+?(?=\||$)", re.DOTALL)
    functions = re.findall(pattern, input_line)
    for i, func in enumerate(functions):
        pattern2 = re.compile(r"(.*) \((.+)\)")
        if mat := re.match(pattern2, func):
            functions[i] = mat.groups()
        else:
            functions[i] = [func, None]
    return functions
