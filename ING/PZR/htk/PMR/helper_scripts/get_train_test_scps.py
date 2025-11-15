#!/usr/bin/env python3
"""
Create .scp files (lists of MFCC feature paths) from .mlf label files.

Usage:
    python make_scp_from_mlf.py --in data/mlfs --out data/scps
"""

import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="Generate .scp lists from .mlf label files (replace .lab → .mfcc)."
    )
    parser.add_argument("--in", dest="in_dir", required=True,
                        help="Input folder containing .mlf files.")
    parser.add_argument("--out", dest="out_dir", required=True,
                        help="Output folder for generated .scp files.")
    args = parser.parse_args()

    in_dir  = Path(args.in_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for mlf in sorted(in_dir.glob("*.mlf")):
        lines = mlf.read_text(encoding="utf-8", errors="ignore").splitlines()
        scp_lines = []

        for line in lines:
            line = line.strip().strip('"')
            if not line.endswith(".lab"):
                continue
            mfcc_path = line.replace(".lab", ".mfcc")
            scp_lines.append(mfcc_path + "\n")

        if not scp_lines:
            print(f"⚠️  Skipping {mlf.name}: no .lab paths found.")
            continue

        scp_path = out_dir / (mlf.stem + ".scp")
        scp_path.write_text("".join(scp_lines), encoding="utf-8")
        print(f"✅ {scp_path} ({len(scp_lines)} entries)")

    print("\nAll SCPs generated successfully.")

if __name__ == "__main__":
    main()
