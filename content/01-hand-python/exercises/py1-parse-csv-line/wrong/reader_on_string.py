import csv


def parse_csv_line(line: str) -> list[str]:
    rows = list(csv.reader(line))
    return rows[0] if rows else []
