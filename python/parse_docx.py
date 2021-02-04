import lxml.etree as etree
import re
from datetime import date

def volume(volume):
    """Args:
        volume (str): Volume to be parsed

    Returns:
        [str]: Number of the volume
        [str]: Title of the volume
        [str]: Date of the volume in the format xxxx-xx-xx/xxxx-xx-xx
        [str]: Rest of the volume
    """
    pattern = re.compile(r"Volume[\n\r\s]+m[sa]. (.+?)\n(.*?)\n(.*?);\n(.*)\n.*?$", re.DOTALL)
    return re.match(pattern, volume).groups()

def split_into_dossiers(volume):
    """Args:
        volume (str): String containg the dossiers to be parsed

    Returns:
        [[str], [str], ...]: List of dossiers
    """
    pattern = re.compile(r"(Dossier.*?(?=Genoemd))", re.DOTALL)
    return re.findall(pattern, volume)

def dossier(dossier):
    """Args:
        dossier (str): Dossier to be parsed

    Returns:
        [str]: Number of the dossier
        [str]: Number of total pages of dosier
        [str]: Title of the dossier
        [str]: Date of the dosier in the format xxxx-xx-xx/xxxx-xx-xx
        [str]: If applicable a description of a sub-section of the dossier, otherwise None
        [bool]: True or None depending on existence of description of file within sub-section
        [str]: Rest of the string (thus, the files)
    """
    pattern = re.compile(r"Dossier (.+) \((.*) bl.\):\n(.*?);\n(.*?);"
                            r"\n*(~.*?;.*?;.*?;)?\n*(In het bijzonder;)?"
                            r"\n*(-.*;)?", re.DOTALL)
    return re.match(pattern, dossier).groups()

def sub_dossier_description(description):
    """Args:
        description (str): Sub-dossier description to be parsed

    Returns:
        [str]: Pages of sub-dossier (x-x)
        [str]: Title of the sub-dossier
        [str]: Place of the sub-dossier
        [str]: Date of the sub-dossier in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"~ bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, description).groups()

def file(file):
    """Args:
        file (str): File  to be parsed

    Returns:
        [str]: Pages of file (x-x)
        [str]: Title of the file
        [str]: Place of the file
        [str]: Date of the file in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"- bl. (.*?): (.*?); \((.*?); (.*?)\);", re.DOTALL)
    return re.match(pattern, file).groups()