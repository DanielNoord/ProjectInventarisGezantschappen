from pathlib import Path

from data_parsing.load_database import initialize_database_for_xml

from util.get_file import maybe_open_file


def _is_persistent(_: str) -> bool:
    return False


def print_all_identifiers(print_to_file: bool) -> None:
    """Print all persistent identifiers."""
    sources: dict[str, str] = {}
    data = initialize_database_for_xml()

    for identifier, individual in data.individuals.items():
        if individual["sources"]:
            for source in individual["sources"]:
                sources[source] = identifier

        if individual["images"]:
            for image in individual["images"]:
                sources[image] = identifier

    with maybe_open_file(
        should_open_file=print_to_file,
        name=Path("outputs") / "non_persistent_sources.md",
    ) as file:
        header = """# Sources and images
| Identifier | Source |
| ------ | ---------- |"""
        print(header, file=file)
        for source, identifier in sorted(sources.items()):
            if _is_persistent(source):
                continue
            print(f"| {identifier} | {source} |", file=file)
