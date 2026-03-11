"""Convert CSV input to a JSON array of objects.

Reads from a filename argument or stdin. Keys come from the CSV header row.
Integers and floats are output as JSON numbers; everything else is a string.
"""

import argparse
import csv
import json
import sys


def infer_value(raw: str) -> int | float | str:
    """Return raw as an int, float, or string, in that order of preference."""
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        pass
    return raw


def csv_to_records(reader: csv.reader) -> list[dict]:  # type: ignore[type-arg]
    """Read a CSV reader into a list of dicts with type-inferred values."""
    rows = list(reader)

    if not rows:
        return []

    headers = rows[0]
    data_rows = rows[1:]

    # A header row that is entirely empty strings with no data rows means
    # there is nothing meaningful to convert — treat as empty input.
    if not headers or all(h == "" for h in headers):
        if not data_rows:
            return []
        print("Error: CSV has no header row.", file=sys.stderr)
        sys.exit(1)

    records = []
    for row in data_rows:
        record = {headers[i]: infer_value(row[i]) for i in range(len(headers))}
        records.append(record)

    return records


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert CSV to a JSON array of objects."
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="Path to CSV file (reads from stdin if omitted)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Indent the JSON output",
    )
    args = parser.parse_args()

    try:
        if args.filename:
            with open(args.filename, encoding="utf-8", newline="") as f:
                reader = csv.reader(f)
                records = csv_to_records(reader)
        else:
            reader = csv.reader(sys.stdin)
            records = csv_to_records(reader)
    except FileNotFoundError:
        print(f"Error: file not found: {args.filename}", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: {args.filename} is a directory, not a file.", file=sys.stderr)
        sys.exit(1)

    indent = 2 if args.pretty else None
    print(json.dumps(records, indent=indent))


if __name__ == "__main__":
    main()
