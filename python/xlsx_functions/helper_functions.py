from openpyxl.cell.cell import Cell


def compare_rows(
    row1: tuple[Cell, ...], row2: tuple[Cell, ...], start_index: int = 1
) -> bool:
    """Compare the values of two rows."""
    return [i.value for i in row1[start_index:]] == [
        i.value for i in row2[start_index:]
    ]


def is_partial_match(row1: tuple[Cell, ...], row2: tuple[Cell, ...]) -> bool:
    """Compare only the title value of two rows."""
    return row1[1].value == row2[1].value
