import re


def sub_series(doss):
    """Args:
        doss (str): String containig all sub-series

    Returns:
        list[(), (), ...]: List of subseries, stored as tuples of (desc, file_desc, files)
    """
    pattern = re.compile(r"(~.*;.*;.*;.*?)\n*$|~", re.DOTALL)
    all_sub_series = re.findall(pattern, doss)
    pattern_2 = re.compile(r"(~.*?:.*?;.*?;.*?;)"
                            r"\n*(In het bijzonder;)?\n*(.*)", re.DOTALL)
    for i, sub in enumerate(all_sub_series):
        all_sub_series[i] = re.match(pattern_2, sub).groups()
    return all_sub_series
