"""Taken from https://github.com/inveniosoftware/idutils."""


def _convert_x_to_10(val: str) -> int:
    """Convert char to int with X being converted to 10."""
    return int(val) if val != "X" else 10


def is_isni(val: str) -> bool:
    """Test if argument is an International Standard Name Identifier."""
    val = val.replace(" ", "").upper()
    if len(val) != 16:
        return False
    try:
        running_total = 0
        for value in val[:-1]:
            running_total = (running_total + int(value)) * 2
        check = (12 - running_total % 11) % 11
        return check == _convert_x_to_10(val[-1])
    except ValueError:
        return False
