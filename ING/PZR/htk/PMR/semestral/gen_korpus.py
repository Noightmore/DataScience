#!/usr/bin/env python3
import argparse
import random
import math
from pathlib import Path


WORDS = [
    "muže",
    "pes",
    "kůň",
    "může",
    "co",
    "kdo",
    "proč",
    "jak",
    "múze",
    "může",
    "může",
    "může",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate a large Czech text file from a fixed set of words."
    )
    p.add_argument(
        "-o", "--output", type=Path, required=True,
        help="Output text file path"
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--lines", type=int,
        help="Number of lines to generate"
    )
    group.add_argument(
        "--megabytes", type=float,
        help="Approximate size of file in megabytes (MiB)"
    )
    p.add_argument(
        "--encoding", type=str, default="utf-8",
        help="Output file encoding (default: utf-8, e.g. cp1250 for HTK-style data)"
    )
    p.add_argument(
        "--min-words-per-line", type=int, default=5,
        help="Minimum words per line (default: 5)"
    )
    p.add_argument(
        "--max-words-per-line", type=int, default=12,
        help="Maximum words per line (default: 12)"
    )
    return p.parse_args()


def estimate_lines_for_size(megabytes: float, encoding: str) -> int:
    """
    Roughly estimate how many lines we need for given size.

    We simulate a few sample lines, encode them, and compute average bytes/line.
    """
    import io

    buf = io.StringIO()
    sample_lines = 1000
    for _ in range(sample_lines):
        n_words = random.randint(5, 12)
        line_words = random.choices(WORDS, k=n_words)
        buf.write(" ".join(line_words) + "\n")

    text = buf.getvalue()
    encoded = text.encode(encoding, errors="ignore")
    avg_bytes_per_line = len(encoded) / sample_lines

    target_bytes = megabytes * 1024 * 1024
    est_lines = int(math.ceil(target_bytes / avg_bytes_per_line))
    return est_lines


def main():
    args = parse_args()

    if args.lines is not None:
        n_lines = args.lines
    else:
        # estimate number of lines for target size
        n_lines = estimate_lines_for_size(args.megabytes, args.encoding)
        print(f"Estimated ~{n_lines} lines for ~{args.megabytes} MiB target.")

    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding=args.encoding, errors="ignore") as f:
        for _ in range(n_lines):
            n_words = random.randint(args.min_words_per_line, args.max_words_per_line)
            # random order of words; can repeat
            line_words = random.choices(WORDS, k=n_words)
            line = " ".join(line_words)
            f.write(line + "\n")

    print(f"Wrote {n_lines} lines to {out} (encoding={args.encoding}).")


if __name__ == "__main__":
    main()
