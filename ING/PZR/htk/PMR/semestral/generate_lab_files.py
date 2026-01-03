#!/usr/bin/env python3
# make_sentence_labs.py
#
# Builds sentence-level .lab files from .txt by:
# 1) loading pseudo dictionary (col1=UPPER_LABEL, col2=PSEUDO_TRANS)
# 2) creating reversed map: pseudo_trans -> label_lower
# 3) for each .txt file: rewrite_text(sentence) -> per-word pseudo transcriptions
# 4) map each pseudo transcription to label and write one label per line into .lab
#
# Uses: from antlr_fun.fun import rewrite_text
#
# Usage:
#   python3 make_sentence_labs.py \
#     --pseudo-dict pseudo_dict.txt \
#     --in data_root \
#     --out out_root \
#     --encoding utf-8 \
#     --lowercase
#
# If unknown pseudos exist:
#   - default: skip that file and print examples
#   - or set --unk <label> to substitute

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Union
import unicodedata
import re


try:
    from antlr_fun.fun import rewrite_text
except Exception as e:
    raise SystemExit(
        "Failed to import rewrite_text from antlr_fun.fun.\n"
        "Make sure your project env / PYTHONPATH is set so `antlr_fun` is importable.\n"
        f"Import error: {e}"
    )


def strip_diacritics(s: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s)
        if not unicodedata.combining(ch)
    )

def parse_args():
    p = argparse.ArgumentParser(
        description="Generate sentence-level HTK .lab files from .txt using reversed pseudo dict (antlr_fun.fun.rewrite_text)."
    )
    p.add_argument("--pseudo-dict", type=Path, required=True,
                   help="Pseudo dict: COL1=UPPER word label, COL2=pseudo transcription, (COL3=count optional).")
    p.add_argument("--in", dest="inp", type=Path, required=True,
                   help="Input root folder containing subfolders with .txt files.")
    p.add_argument("--out", dest="out", type=Path, required=True,
                   help="Output root folder. Structure is mirrored from input.")
    p.add_argument("--encoding", default="utf-8",
                   help="Encoding for reading .txt and pseudo-dict (default: utf-8).")
    p.add_argument("--txt-ext", default=".txt", help="Text file extension (default: .txt).")
    p.add_argument("--lab-ext", default=".lab", help="Output label extension (default: .lab).")
    p.add_argument("--unk", default="",
                   help="If set, unknown pseudo transcriptions map to this label. "
                        "If empty, unknowns cause the file to be skipped with an error.")
    p.add_argument("--lowercase", action="store_true",
                   help="Lowercase the input sentence before rewriting (often useful).")
    p.add_argument("--dry-run", action="store_true", help="Do everything except writing files.")
    return p.parse_args()


def load_reversed_pseudo_dict(path: Path, encoding: str) -> Dict[str, str]:
    """
    Reads pseudo dict lines with >=2 columns:
      COL1 = WORD_LABEL (UPPER in your file)
      COL2 = PSEUDO_TRANSCRIPTION
    Returns: pseudo_transcription -> word_label_lower
    """
    rev: Dict[str, str] = {}
    dup = 0
    bad = 0

    with path.open("r", encoding=encoding, errors="replace") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                bad += 1
                continue

            w_upper = parts[0]
            pseudo = parts[1]
            label = w_upper.lower()

            if pseudo in rev and rev[pseudo] != label:
                dup += 1
                # keep first occurrence
                continue
            rev[pseudo] = label

    if bad:
        print(f"[warn] Skipped {bad} malformed lines in pseudo dict.", file=sys.stderr)
    if dup:
        print(f"[warn] Found {dup} duplicate pseudo keys with conflicting labels (kept first).", file=sys.stderr)

    if not rev:
        raise SystemExit("Reversed pseudo dict is empty. Check file/encoding/format.")
    return rev


def ensure_list(x: Union[List[str], str]) -> List[str]:
    """
    rewrite_text might return:
      - list[str] of per-word pseudo transcriptions
      - OR a single string with space-separated pseudo transcriptions
    Normalize to list[str].
    """
    if isinstance(x, list):
        return [str(t).strip() for t in x if str(t).strip()]
    if isinstance(x, str):
        return [t.strip() for t in x.split() if t.strip()]
    raise TypeError(f"rewrite_text returned unsupported type: {type(x)}")


def main():
    args = parse_args()
    rev = load_reversed_pseudo_dict(args.pseudo_dict, args.encoding)

    in_root = args.inp.resolve()
    out_root = args.out.resolve()

    if not in_root.exists():
        raise FileNotFoundError(f"Input root not found: {in_root}")

    txt_ext = args.txt_ext.lower()
    txt_files = sorted([p for p in in_root.rglob("*") if p.is_file() and p.suffix.lower() == txt_ext])

    if not txt_files:
        raise SystemExit(f"No *{txt_ext} files found under {in_root}")

    ok = 0
    skipped = 0

    for txt_path in txt_files:
        rel = txt_path.relative_to(in_root)
        out_dir = out_root / rel.parent
        out_path = out_dir / (txt_path.stem + args.lab_ext)

        text = txt_path.read_text(encoding="cp1250", errors="replace").strip() #args.encoding
        if args.lowercase:
            text = text.lower()

        # rewrite full sentence -> per-word pseudo transcriptions
        try:
            pseudos = ensure_list(rewrite_text(text))
        except Exception as e:
            print(f"[skip] rewrite_text failed for {txt_path}: {e}", file=sys.stderr)
            skipped += 1
            continue

        labels: List[str] = []
        unknowns: List[str] = []

        for pseudo in pseudos:
            lab = rev.get(pseudo)
            if lab is None:
                if args.unk:
                    lab = args.unk.lower()
                else:
                    unknowns.append(pseudo)
                    continue
            labels.append(lab.lower())

        if unknowns and not args.unk:
            # Fallback: use the ORIGINAL sentence words, normalized (lowercase + strip diacritics),
            # for those positions where pseudo was unknown.
            # We assume rewrite_text preserves token order vs. the original whitespace tokens.
            orig_tokens = re.findall(r"\S+", text)  # uses `text` from above (already lowercased if --lowercase)
            fixed = 0

            for i, pseudo in enumerate(pseudos):
                if pseudo in unknowns:
                    # best-effort: take original token at same index; if not available, use pseudo itself
                    src = orig_tokens[i] if i < len(orig_tokens) else pseudo
                    lab = strip_diacritics(src.lower())
                    labels.append(lab)
                    fixed += 1

            print(f"[unk->label] {txt_path}: fixed {fixed} unknown pseudos (e.g. {unknowns[:8]})",
                  file=sys.stderr)
            # do NOT skip anymore
            unknowns = []

        if not labels:
            print(f"[skip] {txt_path}: no labels produced", file=sys.stderr)
            skipped += 1
            continue

        if args.dry_run:
            print(f"[dry] {txt_path} -> {out_path} ({len(labels)} labels)")
            ok += 1
            continue

        out_dir.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(labels) + "\n", encoding="utf-8")
        ok += 1

    print(f"[done] ok={ok} skipped={skipped} out={out_root}")


if __name__ == "__main__":
    main()
"""
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-03.txt: 1 unknown pseudo transcriptions (e.g. ['ráč'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-06.txt: 1 unknown pseudo transcriptions (e.g. ['sokolofského'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-08.txt: 2 unknown pseudo transcriptions (e.g. ['stác', 'vjetki'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-17.txt: 1 unknown pseudo transcriptions (e.g. ['ubitovatele'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-18.txt: 1 unknown pseudo transcriptions (e.g. ['kojeneckí'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-19.txt: 1 unknown pseudo transcriptions (e.g. ['krokeM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-23.txt: 2 unknown pseudo transcriptions (e.g. ['pjec', 'tejníX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-24.txt: 2 unknown pseudo transcriptions (e.g. ['hotkovic', 'mohelkou'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-31.txt: 1 unknown pseudo transcriptions (e.g. ['tŘímilijonoví'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-37.txt: 2 unknown pseudo transcriptions (e.g. ['zvadlé', 'opadané'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-38.txt: 1 unknown pseudo transcriptions (e.g. ['slétávat'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-64.txt: 2 unknown pseudo transcriptions (e.g. ['vihodnocena', 'hlukeM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-70.txt: 1 unknown pseudo transcriptions (e.g. ['snac'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-76.txt: 2 unknown pseudo transcriptions (e.g. ['jíc', 'tejnou'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-83.txt: 1 unknown pseudo transcriptions (e.g. ['lipencíX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MAR/MAR-91.txt: 1 unknown pseudo transcriptions (e.g. ['pŘitoM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-01.txt: 2 unknown pseudo transcriptions (e.g. ['dlažďicíX', 'seskupuje'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-14.txt: 1 unknown pseudo transcriptions (e.g. ['prohledával'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-15.txt: 1 unknown pseudo transcriptions (e.g. ['špaXtli'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-30.txt: 2 unknown pseudo transcriptions (e.g. ['éfoval', 'roušal'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-38.txt: 1 unknown pseudo transcriptions (e.g. ['brňenskéM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-51.txt: 3 unknown pseudo transcriptions (e.g. ['pozornosc', 'vou', 'tajemnosťí'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/MON/MON-71.txt: 1 unknown pseudo transcriptions (e.g. ['zákazňíkúM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-01.txt: 1 unknown pseudo transcriptions (e.g. ['koupic'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-04.txt: 1 unknown pseudo transcriptions (e.g. ['pokuc'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-05.txt: 2 unknown pseudo transcriptions (e.g. ['procenc', 'tátňího'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-06.txt: 3 unknown pseudo transcriptions (e.g. ['pokuc', 'dvanácc', 'CzeXpointeX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-07.txt: 1 unknown pseudo transcriptions (e.g. ['zájeM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-08.txt: 2 unknown pseudo transcriptions (e.g. ['poCimňíM', 'vistoupeňíM'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-13.txt: 1 unknown pseudo transcriptions (e.g. ['druhovíX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZKS/ZKS-14.txt: 1 unknown pseudo transcriptions (e.g. ['druhovíX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZMK/ZMK-03.txt: 1 unknown pseudo transcriptions (e.g. ['josefofskíX'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZMK/ZMK-20.txt: 1 unknown pseudo transcriptions (e.g. ['naformulovat'])
[skip] /home/rob/Programming/Datascience/ING/PZR/htk/PMR/data/gramy/test_data/ZMK/ZMK-21.txt: 1 unknown pseudo transcriptions (e.g. ['oN'])
"""