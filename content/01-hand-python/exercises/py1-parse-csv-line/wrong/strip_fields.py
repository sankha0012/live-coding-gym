import csv
def parse_csv_line(line: str) -> list[str]:
    rows = list(csv.reader([line]))
    return [f.strip() for f in rows[0]] if rows else []
