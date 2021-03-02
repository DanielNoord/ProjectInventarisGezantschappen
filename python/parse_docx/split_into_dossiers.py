import re


def split_into_dossiers(vol):
    """Args:
        vol (str): String containg the dossiers to be parsed

    Returns:
        list[str, str, ...]: List of dossiers (in string format)
    """
    pattern = re.compile(r"(Dossier.*?(?=Genoemd))", re.DOTALL)
    return re.findall(pattern, vol)
