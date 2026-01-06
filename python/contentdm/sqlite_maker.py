import sqlite3
from pathlib import Path
from types import TracebackType
from typing import Self

from typing_utils.translations_classes import IndividualsDictCleaned

from contentdm.models import FileRow, SeriesRow

_INDIVIDUALS = """
CREATE TABLE individuals (
    identifier TEXT PRIMARY KEY
);
"""

_SERIES = """
CREATE TABLE series (
    identifier TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    title_en TEXT NOT NULL,
    title_nl TEXT NOT NULL,
    title_it TEXT NOT NULL,
    start INTEGER,
    end INTEGER
);
"""

_FILES = """
CREATE TABLE files (
    identifier TEXT PRIMARY KEY,
    series_id TEXT NOT NULL,
    title TEXT NOT NULL,
    title_en TEXT NOT NULL,
    title_nl TEXT NOT NULL,
    title_it TEXT NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    location TEXT,
    FOREIGN KEY (series_id) REFERENCES series (identifier)
);
"""

_SCANS = """
CREATE TABLE scans (
    identifier TEXT NOT NULL,
    file_identifier TEXT NOT NULL,
    FOREIGN KEY (file_identifier) REFERENCES files (identifier)
);
"""

_AUTHORS = """
CREATE TABLE authors (
    individual TEXT NOT NULL,
    file_identifier TEXT NOT NULL,
    FOREIGN KEY (individual) REFERENCES individuals (identifier)
    FOREIGN KEY (file_identifier) REFERENCES files (identifier)
);
"""

_RECIPIENTS = """
CREATE TABLE recipients (
    individual TEXT NOT NULL,
    file_identifier TEXT NOT NULL,
    FOREIGN KEY (individual) REFERENCES individuals (identifier)
    FOREIGN KEY (file_identifier) REFERENCES files (identifier)
);
"""

_SUBJECTS = """
CREATE TABLE subjects (
    individual TEXT NOT NULL,
    file_identifier TEXT NOT NULL,
    FOREIGN KEY (individual) REFERENCES individuals (identifier)
    FOREIGN KEY (file_identifier) REFERENCES files (identifier)
);
"""


class GriglieInserter:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add_series(self, series: SeriesRow) -> None:
        self._connection.execute(
            "INSERT INTO series VALUES(?, ?, ?, ?, ?, ?, ?)",
            (
                series.series_id,
                series.title,
                series.title_en,
                series.title_nl,
                series.title_it,
                series.start,
                series.end,
            ),
        )

    def add_file(self, file: FileRow) -> None:
        self._connection.execute(
            "INSERT INTO files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                file.file_id,
                file.series_id,
                file.title,
                file.title_en,
                file.title_nl,
                file.title_it,
                file.year,
                file.month,
                file.day,
                file.location,
            ),
        )
        self._connection.executemany(
            "INSERT INTO scans VALUES(?, ?)",
            [(s, file.file_id) for s in file.scans],
        )
        self._connection.executemany(
            "INSERT INTO authors VALUES(?, ?)",
            [(a, file.file_id) for a in file.authors],
        )
        self._connection.executemany(
            "INSERT INTO recipients VALUES(?, ?)",
            [(r, file.file_id) for r in file.recipients],
        )
        self._connection.executemany(
            "INSERT INTO subjects VALUES(?, ?)",
            [(s, file.file_id) for s in file.subjects],
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._connection.commit()


class SqliteDatabaseMaker:
    """
    Wrapper to generate the SQLite database for the contentdm files.

    Uses contextmanager protocol(s) to ensure the queries are properly committed and executed in the
    correct order.
    """

    def __init__(self, output_dir: Path) -> None:
        self._connection: sqlite3.Connection | None = None
        self._output_dir = output_dir

    def insert_individuals(self, individuals: IndividualsDictCleaned) -> None:
        assert self._connection is not None, "Use this class as a contextmanager first"
        self._connection.executemany(
            "INSERT INTO individuals VALUES(?)", [(i,) for i in individuals]
        )
        self._connection.commit()

    def __enter__(self) -> SqliteDatabaseMaker:
        (self._output_dir / "delegato.db").write_bytes(b"")

        self._connection = sqlite3.connect(self._output_dir / "delegato.db")
        for table in (
            _INDIVIDUALS,
            _SERIES,
            _FILES,
            _SCANS,
            _AUTHORS,
            _RECIPIENTS,
            _SUBJECTS,
        ):
            self._connection.execute(table)
        self._connection.commit()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        pass

    def griglie(self) -> GriglieInserter:
        assert self._connection is not None, "Use this class as a contextmanager first"
        return GriglieInserter(self._connection)
