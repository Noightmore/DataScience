#!/usr/bin/env python3
"""
make_oov_masked_mlfs.py

Given:
  - a master training MLF (word-level)
  - a folder containing one or more wordlists (*.wlist or any text files)

For each unique wordlist:
  - create a new MLF next to that wordlist (same folder),
  - name it using the wordlist filename,
  - replace any token in the master MLF that is NOT in the wordlist with '!OOV'.

Notes:
  - Keeps the MLF structure exactly (#!MLF!#, "*/xxx.lab", '.' lines).
  - Only masks actual word tokens (non-header, non-quote, non-dot).
"""

import argparse
from pathlib import Path
from typing import Set, List


def load_wordset(wlist_path: Path, encoding: str) -> Set[str]:
    words: Set[str] = set()
    for line in wlist_path.read_text(encoding=encoding, errors="strict").splitlines():
        w = line.strip()
        if not w or w.startswith("#"):
            continue
        words.add(w)
    return words


def mask_mlf(master_lines: List[str], vocab: Set[str], oov_token: str) -> List[str]:
    out: List[str] = []
    for line in master_lines:
        s = line.rstrip("\n")
        t = s.strip()

        # Preserve exact structure lines
        if t == "#!MLF!#" or (t.startswith('"') and t.endswith('"')) or t == "." or t == "":
            out.append(s)
            continue

        # Otherwise treat as a token line
        if t not in vocab:
            out.append(oov_token)
        else:
            out.append(t)

    return out


def main():
    ap = argparse.ArgumentParser(
        description="For each wordlist in a folder, create an OOV-masked copy of a master train.mlf."
    )
    ap.add_argument("--master", type=Path, required=True, help="Master word-level training MLF.")
    ap.add_argument("--wlists", type=Path, required=True, help="Folder containing wordlist files.")
    ap.add_argument("--wlist-exts", nargs="+", default=[".wlist", ".lst", ".txt"],
                    help="Wordlist file extensions to consider (default: .wlist .lst .txt).")
    ap.add_argument("--oov", default="!OOV", help="OOV token to use (default: !OOV).")
    ap.add_argument("--master-encoding", default="utf-8", help="Encoding for master MLF (default: utf-8).")
    ap.add_argument("--wlist-encoding", default="utf-8", help="Encoding for wordlists (default: utf-8).")
    ap.add_argument("--out-encoding", default="utf-8", help="Encoding for output MLFs (default: utf-8).")
    ap.add_argument("--suffix", default="_oovmasked",
                    help="Suffix added to output MLF filename (default: _oovmasked).")
    ap.add_argument("--dry-run", action="store_true", help="Only print what would be written.")
    args = ap.parse_args()

    if not args.master.exists():
        raise SystemExit(f"Missing master MLF: {args.master}")
    if not args.wlists.exists() or not args.wlists.is_dir():
        raise SystemExit(f"Wordlist folder not found / not a dir: {args.wlists}")

    master_text = args.master.read_text(encoding=args.master_encoding, errors="strict")
    master_lines = master_text.splitlines()

    if not master_lines or master_lines[0].strip() != "#!MLF!#":
        raise SystemExit("Master file does not look like an HTK MLF (missing #!MLF!# on first line).")

    exts = {e if e.startswith(".") else "." + e for e in args.wlist_exts}

    wlist_files = sorted([p for p in args.wlists.iterdir() if p.is_file() and p.suffix in exts])
    if not wlist_files:
        raise SystemExit(f"No wordlist files found in {args.wlists} with extensions {sorted(exts)}")

    for wlist_path in wlist_files:
        vocab = load_wordset(wlist_path, args.wlist_encoding)
        vocab.add(args.oov)  # ensure !OOV is always "in vocab" once introduced

        masked_lines = mask_mlf(master_lines, vocab, args.oov)

        # output name: <masterstem>__<wliststem><suffix>.mlf
        out_name = f"{args.master.stem}__{wlist_path.stem}{args.suffix}.mlf"
        out_path = args.wlists / out_name  # save in same folder as input wl folder (per request)

        # stats
        total_tokens = 0
        oov_tokens = 0
        for line in masked_lines:
            t = line.strip()
            if not t or t == "#!MLF!#" or t == "." or (t.startswith('"') and t.endswith('"')):
                continue
            total_tokens += 1
            if t == args.oov:
                oov_tokens += 1

        if args.dry_run:
            print(f"[dry-run] {wlist_path.name} -> {out_path.name} | vocab={len(vocab)} tokens={total_tokens} oov={oov_tokens} ({(oov_tokens/total_tokens if total_tokens else 0):.2%})")
            continue

        out_path.write_text("\n".join(masked_lines) + "\n", encoding=args.out_encoding, newline="\n")
        print(f"[ok] {wlist_path.name} -> {out_path.name} | vocab={len(vocab)} tokens={total_tokens} oov={oov_tokens} ({(oov_tokens/total_tokens if total_tokens else 0):.2%})")


if __name__ == "__main__":
    main()

# python ./mask_mlf_w_wlist.py --master train_master.mlf --wlists ./wlists_mlfs --master-encoding utf-8 --wlist-encoding utf-8 --out-encoding utf-8

"""
[ok] wlist_top10000.wlist -> train_master__wlist_top10000_oovmasked.mlf | vocab=10004 tokens=5919801 oov=1209203 (20.43%)
[ok] wlist_top20000.wlist -> train_master__wlist_top20000_oovmasked.mlf | vocab=20004 tokens=5919801 oov=818053 (13.82%)
[ok] wlist_top60000.wlist -> train_master__wlist_top60000_oovmasked.mlf | vocab=60004 tokens=5919801 oov=344239 (5.82%)
"""