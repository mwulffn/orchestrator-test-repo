"""Count word frequencies in a text file and display the top 10 most common words."""

import argparse
import re
import sys
from collections import Counter
from typing import Iterator


def iter_words(filepath: str) -> Iterator[str]:
    """Yield lowercased words from a file one line at a time."""
    with open(filepath, encoding="utf-8", errors="strict") as f:
        for line in f:
            yield from re.findall(r"[a-z]+", line.lower())


def count_words(filepath: str) -> Counter:
    """Count word frequencies in the given file."""
    return Counter(iter_words(filepath))


def format_table(rows: list[tuple[str, int]]) -> str:
    """Format word/count pairs as a plain-text table."""
    if not rows:
        return ""
    word_col = max(len(word) for word, _ in rows)
    word_col = max(word_col, 4)  # at least as wide as "Word"
    header = f"{'Word':<{word_col}}  Count"
    separator = f"{'-' * word_col}  -----"
    lines = [header, separator]
    for word, count in rows:
        lines.append(f"{word:<{word_col}}  {count}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Count word frequencies in a text file.")
    parser.add_argument("filename", help="Path to the text file to analyse")
    args = parser.parse_args()

    try:
        counts = count_words(args.filename)
    except FileNotFoundError:
        print(f"Error: file not found: {args.filename}", file=sys.stderr)
        sys.exit(1)
    except IsADirectoryError:
        print(f"Error: {args.filename} is a directory, not a file.", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(
            f"Error: {args.filename} does not appear to be a readable text file.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not counts:
        print("The file contains no words.")
        sys.exit(0)

    top10 = counts.most_common(10)
    print(format_table(top10))


if __name__ == "__main__":
    main()
