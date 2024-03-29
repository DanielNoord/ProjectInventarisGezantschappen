import re


def parse_title(input_line: str) -> list[tuple[str, str | None]]:
    """Parses a function string.

    Args:
        input_line: Line to be parsed

    Returns:
        list[tuple[str, Optional[str]]]: List of tuples
            Each tuple contains two strings which are the title and timeperiod of title
    """
    pattern = re.compile(r"\w.+?(?=\||$)", re.DOTALL)
    titles = re.findall(pattern, input_line)
    for i, func in enumerate(titles):
        pattern2 = re.compile(r"(.*) \((.+)\)")
        if mat := re.match(pattern2, func):
            titles[i] = mat.groups()
        else:
            titles[i] = [func, None]
    return titles
