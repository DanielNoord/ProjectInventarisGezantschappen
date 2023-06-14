from typing_utils import DateTuple


def create_date_tuple(
    date: str | DateTuple,
) -> tuple[DateTuple] | tuple[DateTuple, DateTuple]:
    """Creates a tuple of DateTuple's based on an existing DateTuple or date string."""
    if isinstance(date, str):
        # Transform into correct tuple if double date (xxxx-xx-xx/xxxx-xx-xx)
        if "/" in date:
            double_date: list[DateTuple] = []
            double_date_split: list[list[int | None]] = [
                [int(i) for i in j.split("-") if i] for j in date.split("/")
            ]
            for data in double_date_split:
                while len(data) != 3:
                    data.append(None)
                double_date.append(DateTuple(data[0], data[1], data[2]))
            return (double_date[0], double_date[1])

        # Transform into correct tuple if single date (xxxx-xx-xx)
        single_date_split: list[int | None] = [int(i) for i in date.split("-") if i]
        while len(single_date_split) != 3:
            single_date_split.append(None)
        single_date_tuple = DateTuple(
            single_date_split[0], single_date_split[1], single_date_split[2]
        )
        return (single_date_tuple,)

    # Transform into tuple
    return (date,)
