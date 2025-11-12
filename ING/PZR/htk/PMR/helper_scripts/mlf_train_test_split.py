#!/usr/bin/env python3
import argparse
from pathlib import Path
import random
import math

def parse_args():
    p = argparse.ArgumentParser(
        description="Build HTK train/test MLFs from .lab files with include/exclude and ratio splits."
    )
    p.add_argument("--root", type=Path, required=True,
                   help="Start folder to search for .lab files (recursively).")
    p.add_argument("--out", type=Path, default=Path("."),
                   help="Output directory for generated MLFs (default: current dir).")
    p.add_argument("--ext", default=".lab", help="Label file extension (default: .lab).")
    p.add_argument("--encoding", default="cp1250", help="Encoding for reading .lab files (default: cp1250).")
    p.add_argument("--ratios", nargs="+", required=True,
                   help="One or more train:test percentages (NOT normalized). Example: 40:20 80:10")
    p.add_argument("--include", nargs="*", default=[],
                   help="Only keep files whose POSIX path contains ANY of these substrings.")
    p.add_argument("--exclude", nargs="*", default=[],
                   help="Drop files whose POSIX path contains ANY of these substrings.")
    p.add_argument("--seed", type=int, default=42, help="Random seed for shuffling (default: 42).")
    return p.parse_args()

def is_ignored(p: Path) -> bool:
    return any(part == ".ipynb_checkpoints" for part in p.parts)

def collect_lab_files(root: Path, ext: str, include_subs, exclude_subs):
    ext = ext.lower()
    labs = []
    for p in root.rglob(f"*{ext}"):
        if not p.is_file():
            continue
        if is_ignored(p):
            continue
        posix = p.as_posix()
        if include_subs and not any(s in posix for s in include_subs):
            continue
        if exclude_subs and any(s in posix for s in exclude_subs):
            continue
        labs.append(p)
    return sorted(labs)

def label_target_line(root: Path, lab_path: Path) -> str:
    # fixed full path (forward slashes), starting at --root
    rel = lab_path.relative_to(root)
    full = (root / rel).as_posix()
    return f"\"{full}\"\n"

def write_mlf(root: Path, paths, out_path: Path, lab_encoding: str):
    lines = ["#!MLF!#\n"]
    for lab in paths:
        lines.append(label_target_line(root, lab))
        txt = lab.read_text(encoding=lab_encoding, errors="strict")
        if not txt.endswith("\n"):
            txt += "\n"
        lines.append(txt)
        lines.append(".\n")
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {len(paths):5d} utterances → {out_path}")

def parse_ratio_str_direct(r: str):
    # Accepts "a:b" or "a/b" as direct percentages (not normalized).
    r = r.replace("/", ":")
    parts = r.split(":")
    if len(parts) != 2:
        raise ValueError(f"Ratio must be TRAIN:TEST (got '{r}')")
    tr, te = [float(x) for x in parts]
    if tr < 0 or te < 0:
        raise ValueError(f"Negative percentage in '{r}'")
    if tr + te > 100.0 + 1e-9:
        raise ValueError(f"Train+test exceeds 100%: {tr}+{te} in '{r}'")
    return tr, te

def split_train_test_partial(items, train_pct, test_pct, seed=42):
    """Sample train from all, then test from the remainder, using given percentages of the FULL set."""
    n = len(items)
    rng = random.Random(seed)
    items = items[:]  # copy
    rng.shuffle(items)

    # sizes (round to nearest, but never exceed)
    train_n = int(round(n * (train_pct / 100.0)))
    train_n = min(train_n, n)

    remaining = n - train_n
    test_n = int(round(n * (test_pct / 100.0)))
    test_n = min(test_n, remaining)

    train = items[:train_n]
    test  = items[train_n:train_n + test_n]
    return train, test

def main():
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    labs = collect_lab_files(args.root, args.ext, args.include, args.exclude)
    if not labs:
        raise SystemExit(f"No {args.ext} files found under {args.root.resolve()} "
                         f"(after include/exclude filtering).")

    print(f"Found {len(labs)} {args.ext} files under {args.root}")
    if args.include:
        print(f" include filters: {args.include}")
    if args.exclude:
        print(f" exclude filters: {args.exclude}")

    for r in args.ratios:
        train_pct, test_pct = parse_ratio_str_direct(r)
        ratio_tag = f"{int(train_pct)}-{int(test_pct)}"

        train, test = split_train_test_partial(labs, train_pct, test_pct, seed=args.seed)

        train_mlf = args.out / f"train_phones_{ratio_tag}.mlf"
        test_mlf  = args.out / f"test_phones_{ratio_tag}.mlf"

        write_mlf(args.root, train, train_mlf, args.encoding)
        write_mlf(args.root, test,  test_mlf,  args.encoding)

        covered = (len(train) + len(test)) / len(labs) * 100.0
        print(f"Ratio {train_pct:.1f}:{test_pct:.1f} → "
              f"train={len(train)}, test={len(test)}, covered={covered:.1f}% "
              f"(omitted={len(labs) - len(train) - len(test)})\n")

if __name__ == "__main__":
    main()
