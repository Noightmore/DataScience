#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Dict

# ----------------- settings -----------------
data_dir = Path("data")   # root to scan recursively
phn_ext  = ".phn"         # input phone files (CP1250)
lab_ext  = ".lab"         # output label files (CP1250)
verbose_list_files = False  # set True to list every .phn in each dir
enforce_edge_hyphens = False  # set True to force leading/trailing '-' around the sequence
# --------------------------------------------

# mapping: (phn char) -> (label symbol)
PHONEME_MAP: Dict[str, str] = {
    "a": "a",  "á": "aa",
    "b": "b",
    "c": "ts", "C": "dz",
    "č": "ch", "Č": "dg",
    "d": "d",  "ď": "dj",
    "e": "e",  "é": "ee",
    "f": "f",
    "g": "g",
    "h": "h",  "X": "x",
    "i": "i",  "í": "ii",
    "j": "y",
    "k": "k",
    "l": "l",
    "m": "m",  "M": "mg",
    "n": "n",  "N": "ng",
    "ň": "nj",
    "o": "o",  "ó": "oo",
    "p": "p",
    "r": "r",
    "ř": "rz", "Ř": "rs",
    "s": "s",  "š": "sh",
    "t": "t",  "ť": "tj",
    "u": "u",  "ú": "uu",
    "v": "v",
    "z": "z",  "ž": "zh",
    "-": "si",
    "E": "swa",
    "1": "si", "2": "si", "3": "si", "4": "si", "5": "si", "0": "si",
}

# characters to silently drop from .phn (e.g., underscores)
IGNORED_CHARS = {"_"}

def phn_to_lab_lines(phn_cp1250: str) -> list[str]:
    """
    Convert a .phn text into '0 0 <mapped>' lines.
    - strip whitespace
    - drop IGNORED_CHARS (e.g., '_')
    - optionally enforce leading/trailing '-'
    - map each remaining char via PHONEME_MAP
    """
    # remove whitespace/newlines
    raw = "".join(ch for ch in phn_cp1250 if not ch.isspace())
    # drop ignored chars (like underscores)
    seq = "".join(ch for ch in raw if ch not in IGNORED_CHARS)

    if enforce_edge_hyphens:
        # wrap with '-' but avoid duplicates if already present
        seq = "-" + seq.strip("-") + "-"

    lines: list[str] = []
    for idx, ch in enumerate(seq):
        mapped = PHONEME_MAP.get(ch)
        if mapped is None:
            cp = f"U+{ord(ch):04X}"
            raise ValueError(f"Unmapped character {ch!r} ({cp}) at position {idx}")
        lines.append(f"0 0 {mapped}\n")
    return lines

def generate_lab_for_phn(phn_path: Path) -> Path:
    lab_path = phn_path.with_suffix(lab_ext)
    phn_text = phn_path.read_text(encoding="cp1250")   # PHN is CP1250
    lab_lines = phn_to_lab_lines(phn_text)
    lab_path.write_text("".join(lab_lines), encoding="cp1250")  # LAB in CP1250
    return lab_path

def main():
    total_dirs = 0
    total_phn  = 0
    made_lab   = 0
    skipped    = 0
    errors     = []

    for dirpath, dirnames, filenames in os.walk(data_dir):
        total_dirs += 1
        d = Path(dirpath)
        phn_files = [fn for fn in filenames if fn.lower().endswith(phn_ext)]
        print(f"[dir] {d.as_posix()}  | subdirs: {len(dirnames):>3}  | files: {len(filenames):>4}  | .phn here: {len(phn_files):>3}")
        if verbose_list_files and phn_files:
            for fn in phn_files:
                print("      └─", fn)

        for fn in phn_files:
            total_phn += 1
            phn_path = d / fn
            try:
                lab_path = generate_lab_for_phn(phn_path)
                made_lab += 1
                print(f"  [+] {phn_path.name} → {lab_path.name}")
            except Exception as e:
                skipped += 1
                errors.append((phn_path, str(e)))
                print(f"  [!] SKIP {phn_path.name}: {e}")

    print("\nSummary")
    print(f"  Visited directories : {total_dirs}")
    print(f"  .phn found          : {total_phn}")
    print(f"  .lab generated      : {made_lab}")
    print(f"  Errors/Skipped      : {skipped}")

    if errors:
        print("\nFirst few errors for debugging:")
        for p, msg in errors[:10]:
            print(" -", p.as_posix(), "->", msg)

if __name__ == "__main__":
    main()
