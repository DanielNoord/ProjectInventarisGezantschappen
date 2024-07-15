from collections.abc import Iterator
from contextlib import contextmanager
from io import TextIOWrapper
from pathlib import Path


@contextmanager
def maybe_open_file(should_open_file: bool, name: Path) -> Iterator[TextIOWrapper | None]:
    """Open and close a file if necessary, otherwise yield None."""
    if not should_open_file:
        yield None
        return

    file = open(name, "w", encoding="utf-8")
    yield file
    file.close()
