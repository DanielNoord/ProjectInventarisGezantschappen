import argparse
from enum import StrEnum
from typing import assert_never

from util.biographies import export_biographies
from util.partial_matches import PartialMatcher
from util.persistent_identifiers import print_all_identifiers


class Command(StrEnum):
    """All supported commands."""

    EXPORT_BIOGRAPHIES = "export-biographies"
    FIND_PARTIAL_MATCHES = "find-partial-matches"
    PERSISTENT_IDENTIFIERS = "persistent-identifiers"


def _main() -> None:
    """Main logic of the script."""
    # Arguments shared by all programs
    parser = argparse.ArgumentParser(
        description="Some utility scripts to quickly print or write data."
    )
    parser.add_argument("--print-to-file", action=argparse.BooleanOptionalAction)

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser(Command.PERSISTENT_IDENTIFIERS)
    subparsers.add_parser(Command.EXPORT_BIOGRAPHIES)
    partial_match = subparsers.add_parser(Command.FIND_PARTIAL_MATCHES)
    partial_match.add_argument("--sanitize", action=argparse.BooleanOptionalAction)

    # Logic to execute correct command
    arguments = parser.parse_args()

    command = Command(arguments.command)
    match command:
        case Command.PERSISTENT_IDENTIFIERS:
            print_all_identifiers(arguments.print_to_file)
        case Command.EXPORT_BIOGRAPHIES:
            export_biographies(arguments.print_to_file)
        case Command.FIND_PARTIAL_MATCHES:
            matcher = PartialMatcher()
            matcher.run(arguments.print_to_file, arguments.sanitize)
        case _:
            assert_never(command)


if __name__ == "__main__":
    _main()
