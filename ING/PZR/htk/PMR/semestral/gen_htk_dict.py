#!/usr/bin/env python3
# build_htk_dicts.py
#
# Input format per line (tab or spaces):
#   COL1_UPPER  COL2_PSEUDOPHONES  COL3_COUNT
#
# Produces (ASCII-sorted) HTK-style dict + wordlist for top 10k/20k/60k by count.
#
# Usage:
#
#   python ./gen_htk_dict.py --in dict_test.cz --out test_dicts --strict --min_count 30
#  mincount zmenen na 5, vyjde na 60K unikatnich slov presne
#
# Outputs:
#   outdir/dict_top10000.dic
#   outdir/wlist_top10000.wlist
#   outdir/dict_top20000.dic
#   outdir/wlist_top20000.wlist
#   outdir/dict_top60000.dic
#   outdir/wlist_top60000.wlist

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Tuple


PHONEME_MAP: Dict[str, str] = {
    "a": "a",
    "á": "aa",
    'ä': "aa",
    "b": "b",
    "c": "ts",
    "C": "dz",
    "č": "ch",
    "Č": "dg",
    'ç': "ts",
    "d": "d",
    "ď": "dj",
    "e": "e",
    "é": "ee",
    'ě': "ee",
    'ë': "ee",
    'ę': "ee",
    "f": "f",
    "g": "g",
    "h": "h",
    "X": "x",
    "i": "i",
    "í": "ii",
    "j": "y",
    "k": "k",
    "l": "l",
    'ľ': "l",
    'ł': "l",
    "m": "m",
    "M": "mg",
    "n": "n",
    'ń': "n",
    "N": "ng",
    "ň": "nj",
    "o": "o",
    "ó": "oo",
    'ö': "oo",
    "p": "p",
    "r": "r",
    "ř": "rz",
    "Ř": "rs",
    "s": "s",
    'ß': "s",
    "š": "sh",
    "t": "t",
    "ť": "tj",
    "u": "u",
    "ü": "uu",
    "ú": "uu",
    "v": "v",
    "z": "z",
    "ž": "zh",
    "-": "si",
    "E": "swa",
    "1": "si",
    "2": "si",
    "3": "si",
    "4": "si",
    "5": "si",
    "0": "si",
}

# Special tokens you want always present in vocab + dict
SPECIAL_WORDS = ["!ENTER", "!EXIT", "!OOV", "!SIL"]
SPECIAL_PRON = "si"  # map all of them to model 'sil'


def parse_args():
    p = argparse.ArgumentParser(
        description="Create HTK dict + wordlists for top-N words from a freq dictionary file."
    )
    p.add_argument("--in", dest="inp", type=Path, required=True,
                   help="Input file with 3 columns: UPPER, pseudo, count.")
    p.add_argument("--out", dest="out", type=Path, required=True,
                   help="Output directory.")
    p.add_argument("--encoding", default="utf-8",
                   help="Input file encoding (default: utf-8). Use cp1250 if needed.")
    p.add_argument("--sizes", nargs="+", type=int, default=[10000, 20000, 60000],
                   help="Top-N sizes to generate (default: 10000 20000 60000).")
    p.add_argument("--strict", action="store_true",
                   help="Fail on unknown pseudo-phones instead of skipping lines.")
    p.add_argument("--min_count", type=int, default=0,
                   help="Optional: ignore entries with count < min_count (default: 0).")
    return p.parse_args()


def ascii_key(s: str) -> bytes:
    return s.encode("ascii", errors="replace")


def transform_pseudo_to_htk(pseudo: str) -> List[str]:
    phones: List[str] = []
    for ch in pseudo:
        if ch.isspace():
            continue
        if ch not in PHONEME_MAP:
            raise KeyError(ch)
        phones.append(PHONEME_MAP[ch])
    return phones


def read_entries(path: Path, encoding: str, strict: bool, min_count: int) -> List[Tuple[int, str, str]]:
    """
    Returns list of (count, label_lower, pseudo)
    label_lower = lowercased COL1
    pseudo = COL2 string
    """
    entries: List[Tuple[int, str, str]] = []
    bad = 0

    with path.open("r", encoding=encoding, errors="replace") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) < 3:
                bad += 1
                if strict:
                    raise ValueError(f"Line {ln}: expected 3 columns, got: {parts}")
                continue

            w_upper, pseudo, cnt_str = parts[0], parts[1], parts[2]
            try:
                cnt = int(cnt_str)
            except ValueError:
                bad += 1
                if strict:
                    raise ValueError(f"Line {ln}: count is not int: {cnt_str}")
                continue

            if cnt < min_count:
                continue

            label = w_upper.lower()

            # Avoid accidental collision with our special tokens
            if label.upper() in SPECIAL_WORDS:
                # skip it; we'll add specials ourselves deterministically
                continue

            # Validate/transform pseudo now (so we can skip early if not strict)
            try:
                _ = transform_pseudo_to_htk(pseudo)
            except KeyError as e:
                bad += 1
                if strict:
                    raise ValueError(f"Line {ln}: unknown pseudo phone char: {e.args[0]!r} in {pseudo!r}")
                continue

            entries.append((cnt, label, pseudo))

    if bad:
        print(f"[warn] Skipped {bad} bad/unknown lines (use --strict to fail).", file=sys.stderr)
    return entries


def write_dict_and_wlist(outdir: Path, top_items: List[Tuple[int, str, str]], tag: str):
    """
    top_items are (count, label, pseudo)
    writes:
      dict_top{tag}.dic   with lines:  label  <htk phones...>
      wlist_top{tag}.wlist with lines: label
    """
    # Sort ASCII by word label (HTK-ish)
    top_items_sorted = sorted(top_items, key=lambda x: ascii_key(x[1]))

    dict_path = outdir / f"dict_top{tag}.dic"
    wlist_path = outdir / f"wlist_top{tag}.wlist"

    with dict_path.open("w", encoding="utf-8", newline="\n") as fd, \
            wlist_path.open("w", encoding="utf-8", newline="\n") as fw:

        # normal words
        for cnt, label, pseudo in top_items_sorted:
            phones = transform_pseudo_to_htk(pseudo)
            fd.write(f"{label}\t{' '.join(phones)}\n")
            fw.write(f"{label}\n")

        # specials at the end
        for w in SPECIAL_WORDS:
            fd.write(f"{w}\t{SPECIAL_PRON}\n")
            fw.write(f"{w}\n")


def main():
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    sizes = sorted(set(args.sizes))
    max_n = max(sizes)

    entries = read_entries(args.inp, args.encoding, args.strict, args.min_count)
    if not entries:
        raise SystemExit("No valid entries read from input file.")

    # Sort by count desc, then stable by label (for reproducibility)
    entries.sort(key=lambda x: (-x[0], x[1]))

    top_max = entries[:max_n]

    for n in sizes:
        subset = top_max[:n]
        write_dict_and_wlist(args.out, subset, str(n))
        print(f"[ok] Wrote top {n}: dict + wlist into {args.out}")

    print("[done]")


if __name__ == "__main__":
    main()

