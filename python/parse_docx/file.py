import re


def file(input_file):
    """Args:
        input_file (str): File  to be parsed

    Returns:
        str: Pages of file (x-x)
        str: Title of the file
        str: Place of the file
        str: Date of the file in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"- bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, input_file).groups()
