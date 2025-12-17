import re

ERR = (-1, "ERR")


def read_file_to_string(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()


def parse_into_lines(file: str) -> list[str]:
    return [line for line in file.splitlines() if line.strip()]


def parse_line_to_count_and_card_title(line: str) -> tuple[int, str]:
    pattern_count_cardname: re.Pattern = re.compile(r"^([0-9]{1,2})\s(.*)$")
    line_match = pattern_count_cardname.match(line)
    if not line_match:
        print(f"[ERROR] parsing line {line}; No matches found")
        return ERR
    group_raw: tuple = line_match.groups()
    if not group_raw[0]:
        print(f"[ERROR] parsing line {line}; No count found")
        return ERR
    try:
        return int(group_raw[0]), group_raw[1]
    except Exception as e:
        print(f"[ERROR] parsing line {line} with exception:\n {e}")
        return ERR
