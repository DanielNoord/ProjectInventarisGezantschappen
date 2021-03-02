import re


def volume(vol):
    """Args:
        vol (str): Volume to be parsed

    Returns:
        str: Number of the volume
        str: Title of the volume
        str: Date of the volume in the format xxxx-xx-xx/xxxx-xx-xx
    """
    pattern = re.compile(r"Volume[\n\r\s]+m[sa]. (.+?)\n(.*?)\n(.*?);\n.*?$", re.DOTALL)
    return re.match(pattern, vol).groups()
