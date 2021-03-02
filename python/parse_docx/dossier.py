import re


def dossier(doss):
    """Args:
        doss (str): Dossier to be parsed

    Returns:
        str: Number of the dossier
        str: Number of total pages of dosier
        str: Title of the dossier
        str: Date of the dosier in the format xxxx-xx-xx/xxxx-xx-xx
        str: If applicable the sub-sections of the dossier, otherwise None
        str: Rest of the string (thus, the files)
    """
    pattern = re.compile(r"Dossier (.+) \((.*) bl.\):\n(.*?);\n(.*?);"
                            r"\n*(~.*?;.*?;.*?;.*)*"
                            r"\n*(-.*;)?", re.DOTALL)
    return re.match(pattern, doss).groups()
