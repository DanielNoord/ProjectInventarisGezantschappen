import re


def function(input_line):
    """Args:
        input_line (str): Line to be parsed

    Returns:
        list[[], [], [], ...]: List of lists
            [str, str] Each list contains two strings which are:
                str: Title of function
                str: Timeperiod of function
    """
    pattern = re.compile(r"\w.+?(?=\||$)", re.DOTALL)
    functions = re.findall(pattern, input_line)
    for i, func in enumerate(functions):
        pattern2 = re.compile(r"(.*) \((.+)\)")
        if re.match(pattern2, func):
            functions[i] = re.match(pattern2, func).groups()
        else:
            functions[i] = [func, None]
    return functions
