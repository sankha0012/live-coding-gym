import csv
def parse_csv_line(line: str) -> list[str]:
    rows = list(csv.reader([line], skipinitialspace=True))
    return rows[0] if rows else []
