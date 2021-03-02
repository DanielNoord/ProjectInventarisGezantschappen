import re


def sub_dossier_description(desc):
    """Args:
        desc (str): Sub-dossier description to be parsed

    Returns:
        str: Pages of sub-dossier (x-x)
        str: Title of the sub-dossier
        str: Place of the sub-dossier
        str: Date of the sub-dossier in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"~ bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, desc).groups()
