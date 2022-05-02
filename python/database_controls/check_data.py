from date_functions import extract_date


def control_date(timeperiod: str) -> None:
    """Controls date be calling extract_date() which raises exceptions for certain errors.

    Args:
        timeperiod: String representation in standard date form
    """
    assert extract_date(timeperiod, "nl_NL")
