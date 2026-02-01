#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys
import re

# Import your G2P function from the script you pasted
# (make sure run_translator.py is on PYTHONPATH or in the same folder)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PMR.antlr_fun.fun import rewrite_text

def parse_args():
    p = argparse.ArgumentParser(
        description=(
            "Scan .txt files, collect unique words, run them through "
            "G2P (rewrite_text) and save a helper dict."
        )
    )
    p.add_argument(
        "--root",
        type=Path,
        required=True,
        help="Root directory to recursively scan for .lab files.",
    )
    p.add_argument(
        "--temp_path",
        type=Path,
        required=True,
        help="Directory where the helper dict will be stored.",
    )
    p.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Directory for later final outputs (HTK dict, wlist, etc.). "
             "Currently unused – reserved for next steps.",
    )
    return p.parse_args()


def collect_unique_words(root: Path, encoding: str = "cp1250") -> set[str]:
    """
    Walks 'root', finds all *.lab files and collects all unique tokens.
    Lab files are assumed to be plain text in 'encoding', with words
    separated by whitespace (spaces/newlines).
    """
    if not root.exists():
        sys.exit(f"--root path does not exist: {root}")

    lab_paths = sorted(root.rglob("*.txt"))
    if not lab_paths:
        print(f"No .lab files found under {root}", file=sys.stderr)
        return set()

    word_re = re.compile(r"\S+")  # any non-whitespace sequence
    words: set[str] = set()

    for lab in lab_paths:
        try:
            text = lab.read_text(encoding=encoding)
        except UnicodeDecodeError as e:
            print(f"[warn] Could not read {lab} as {encoding}: {e}", file=sys.stderr)
            continue

        for m in word_re.finditer(text):
            token = m.group(0).strip()
            if not token:
                continue
            # You can add filters here later, e.g. skip pure numbers:
            # if token.isdigit(): continue
            words.add(token)

    return words


def build_helper_dict(words: set[str]) -> dict[str, str]:
    """
    For each word, run the G2P 'rewrite_text' and store the result.
    We call rewrite_text on a single word at a time, so cross-word
    assimilation rules won't interfere.
    """
    helper = {}
    for w in sorted(words):
        # G2P may return leading/trailing spaces; strip them just in case.
        g2p = rewrite_text(w).strip()
        helper[w] = g2p
    return helper


def write_helper_dict(helper: dict[str, str], temp_path: Path, filename: str = "helper.dict"):
    """
    Writes the helper dict as:  word<TAB>g2p_output  (UTF-8).
    """
    temp_path.mkdir(parents=True, exist_ok=True)
    out_file = temp_path / filename

    with out_file.open("w", encoding="utf-8") as f:
        for word in sorted(helper.keys()):
            f.write(f"{word}\t{helper[word]}\n")

    print(f"Wrote helper dict with {len(helper)} entries to {out_file}")


def main():
    args = parse_args()
    words = collect_unique_words(args.root, encoding="cp1250")
    if not words:
        print("No words collected; nothing to do.", file=sys.stderr)
        return

    print(f"Collected {len(words)} unique word(s) from .lab files.")

    helper = build_helper_dict(words)
    write_helper_dict(helper, args.temp_path)

    # 'args.out' is kept for the next step (final HTK dict + wlist).
    # We'll add that logic once you specify the rest of the program.


if __name__ == "__main__":
    main()
