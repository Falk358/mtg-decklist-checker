import re


def read_file_to_string(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()


def parse_into_lines(file: str) -> list[str]:
    lines_parsed: list[str] = [line for line in file.splitlines()]
    empty_lines_removed: list[str] = list(filter(lambda x: x != "", lines_parsed))
    return empty_lines_removed
