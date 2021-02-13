import re

def volume(vol):
    """Args:
        vol (str): Volume to be parsed

    Returns:
        [str]: Number of the volume
        [str]: Title of the volume
        [str]: Date of the volume in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"Volume[\n\r\s]+m[sa]. (.+?)\n(.*?)\n(.*?);\n.*?$", re.DOTALL)
    return re.match(pattern, vol).groups()

def split_into_dossiers(vol):
    """Args:
        vol (str): String containg the dossiers to be parsed

    Returns:
        [[str], [str], ...]: List of dossiers
    """
    pattern = re.compile(r"(Dossier.*?(?=Genoemd))", re.DOTALL)
    return re.findall(pattern, vol)

def dossier(doss):
    """Args:
        doss (str): Dossier to be parsed

    Returns:
        [str]: Number of the dossier
        [str]: Number of total pages of dosier
        [str]: Title of the dossier
        [str]: Date of the dosier in the format xxxx-xx-xx/xxxx-xx-xx
        [str]: If applicable the sub-sections of the dossier, otherwise None
        [str]: Rest of the string (thus, the files)
    """
    pattern = re.compile(r"Dossier (.+) \((.*) bl.\):\n(.*?);\n(.*?);"
                            r"\n*(~.*?;.*?;.*?;.*)*"
                            r"\n*(-.*;)?", re.DOTALL)
    return re.match(pattern, doss).groups()

def sub_series(doss):
    """Args:
        doss (str): String containig all sub-series

    Returns:
        [list]: List of subseries, stored as tuples of (desc, file_desc, files)
    """
    pattern = re.compile(r"(~.*;.*;.*;.*?)\n*$|~", re.DOTALL)
    all_sub_series = re.findall(pattern, doss)
    pattern_2 = re.compile(r"(~.*?:.*?;.*?;.*?;)"
                            r"\n*(In het bijzonder;)?\n*(.*)", re.DOTALL)
    for i, sub in enumerate(all_sub_series):
        all_sub_series[i] = re.match(pattern_2, sub).groups()
    return all_sub_series

def sub_dossier_description(desc):
    """Args:
        desc (str): Sub-dossier description to be parsed

    Returns:
        [str]: Pages of sub-dossier (x-x)
        [str]: Title of the sub-dossier
        [str]: Place of the sub-dossier
        [str]: Date of the sub-dossier in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"~ bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, desc).groups()

def file(input_file):
    """Args:
        input_file (str): File  to be parsed

    Returns:
        [str]: Pages of file (x-x)
        [str]: Title of the file
        [str]: Place of the file
        [str]: Date of the file in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"- bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, input_file).groups()

def person(input_line):
    """Args:
        input_line (str): Line to be parsed

    Returns:
        [str]: Surname
        [str]: Name
        [str]: Nationality
        [str]: Title
        [str]: Function
        [str]: Place of residence
    """
    pattern = re.compile(r"- (.*); (.*); (.*); (.*); (.*); (.*);;", re.DOTALL)
    return re.match(pattern, input_line).groups()

def function(input_line):
    """Args:
        input_line (str): Line to be parsed

    Returns:
        [list]: List of functions, stored as lists of [title, timeperiod] stored as strings
    """
    pattern = re.compile(r"\w.+?(?=,|$)", re.DOTALL)
    functions = re.findall(pattern, input_line)
    for i, func in enumerate(functions):
        pattern2 = re.compile(r"(.*) \((.+)\)")
        if re.match(pattern2, func):
            functions[i] = re.match(pattern2, func).groups()
        else:
            functions[i] = [func, None]
    return functions
