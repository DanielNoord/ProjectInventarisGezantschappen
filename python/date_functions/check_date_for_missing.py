from datetime import date


def check_date_for_missing_elements(
    year: date | str | float | None,
    month: date | str | float | None,
    day: date | str | float | None,
    doc_number: date | str | float | None,
) -> None:
    """Check for inconsistencies in document dates."""
    if day and not month:
        raise ValueError(f"Document has day but no month, see: {doc_number}")
    if day and not year:
        raise ValueError(f"Document has day but no year, see: {doc_number}")
    if month and not year:
        raise ValueError(f"Document has month but no year, see: {doc_number}")
    if any(isinstance(i, date) for i in (year, month, day)):
        raise TypeError(
            f"Some argument of document date isn't an integer, see: {doc_number}"
        )
