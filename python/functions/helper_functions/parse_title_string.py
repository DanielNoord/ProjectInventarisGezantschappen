import re


def title(input_line):
    """Parses a function string

    Args:
        input_line (str): Line to be parsed

    Returns:
        list[[], [], [], ...]: List of lists
            [str, str] Each list contains two strings which are:
                str: Title of title
                str: Timeperiod of title
    """
    pattern = re.compile(r"\w.+?(?=\||$)", re.DOTALL)
    titles = re.findall(pattern, input_line)
    for i, func in enumerate(titles):
        pattern2 = re.compile(r"(.*) \((.+)\)")
        if re.match(pattern2, func):
            titles[i] = re.match(pattern2, func).groups()
        else:
            titles[i] = [func, None]
    return titles
