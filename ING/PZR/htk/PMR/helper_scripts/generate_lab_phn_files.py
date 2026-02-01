#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict

# ---- import your G2P here ----
# It must accept a *punctuation/whitespace-stripped* sentence and return a phoneme string
from ING.PMR.antlr_fun.fun import rewrite_text

# ---- settings ----
root_data = Path("data")
test_root = root_data / "Test"     # process ONLY this subtree
txt_ext   = ".txt"
phn_ext   = ".phn"
lab_ext   = ".lab"
encoding  = "cp1250"               # CP1250 for .txt/.phn/.lab
add_edge_hyphens = True            # enforce leading/trailing '-' in .phn

# --- mapping: .phn char -> .lab symbol ---
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
IGNORED_CHARS = {"_"}  # silently drop underscores when building .lab

def clean_for_g2p(text: str) -> str:
    """Strip whitespace and punctuation before passing to rewrite_text()."""
    no_ws = re.sub(r"\s+", "", text)
    no_punct = re.sub(r"[.,!?;:„“\"'()\-–—]", "", no_ws)
    return no_punct

def build_phn_from_txt(txt_path: Path, phn_path: Path) -> str:
    """Create .phn (CP1250) from .txt using rewrite_text(). Return the phn string."""
    sentence = txt_path.read_text(encoding=encoding, errors="strict")
    g2p_in = clean_for_g2p(sentence)
    phn_str = rewrite_text(g2p_in).rstrip("\n")
    if add_edge_hyphens:
        phn_str = f"-{phn_str.strip('-')}-"
    phn_path.write_text(phn_str + "\n", encoding=encoding)
    return phn_str

def phn_to_lab_lines(phn_str: str) -> list[str]:
    """Convert a phn string to '0 0 <mapped>' lines (CP1250 output)."""
    # remove whitespace; drop underscores
    seq = "".join(ch for ch in phn_str if not ch.isspace())
    seq = "".join(ch for ch in seq if ch not in IGNORED_CHARS)
    lines: list[str] = []
    for idx, ch in enumerate(seq):
        mapped = PHONEME_MAP.get(ch)
        if mapped is None:
            cp = f"U+{ord(ch):04X}"
            raise ValueError(f"Unmapped character {ch!r} ({cp}) at position {idx} in {phn_str!r}")
        lines.append(f"0 0 {mapped}\n")
    return lines

def ensure_lab_from_phn(phn_path: Path, lab_path: Path):
    """Create/overwrite .lab (CP1250) from an existing .phn file."""
    phn_str = phn_path.read_text(encoding=encoding, errors="strict")
    lab_lines = phn_to_lab_lines(phn_str)
    lab_path.write_text("".join(lab_lines), encoding=encoding)

def main():
    if not test_root.exists():
        raise SystemExit(f"Test root does not exist: {test_root}")

    made_phn = made_lab = used_existing_phn = 0
    skipped_txt = 0
    errors = []

    # Walk only data/Test/**
    for dirpath, _, filenames in os.walk(test_root):
        d = Path(dirpath)
        txts = [d / f for f in filenames if f.lower().endswith(txt_ext)]
        # Optional: print progress per folder
        print(f"[dir] {d.as_posix()}  | txt here: {len(txts):>3}")
        for txt in txts:
            stem = txt.with_suffix("")  # same basename
            phn_path = stem.with_suffix(phn_ext)
            lab_path = stem.with_suffix(lab_ext)
            try:
                if not phn_path.exists():
                    # build .phn from .txt (G2P)
                    phn_str = build_phn_from_txt(txt, phn_path)
                    made_phn += 1
                    print(f"  [+] phn: {phn_path.name}")
                else:
                    used_existing_phn += 1
                    # also pick up its content (for lab generation below)
                    phn_str = phn_path.read_text(encoding=encoding, errors="strict")

                # always (re)create .lab from whatever phn we have now
                lab_lines = phn_to_lab_lines(phn_str)
                lab_path.write_text("".join(lab_lines), encoding=encoding)
                made_lab += 1
                print(f"  [+] lab: {lab_path.name}")

            except Exception as e:
                errors.append((txt, str(e)))
                skipped_txt += 1
                print(f"  [!] SKIP {txt.name}: {e}")

    print("\nSummary")
    print(f"  .phn created          : {made_phn}")
    print(f"  .phn already existed  : {used_existing_phn}")
    print(f"  .lab written          : {made_lab}")
    print(f"  .txt skipped (errors) : {skipped_txt}")

    if errors:
        print("\nFirst few errors:")
        for p, msg in errors[:10]:
            print(" -", p.as_posix(), "->", msg)

if __name__ == "__main__":
    main()
