from pathlib import Path

# ---- tweak these if needed ----
root = Path(".")             # project root (where data/ lives)
data_dir = root / "data"     # input WAV tree
out_scp  = root / "mfcc.lst" # where to write the HCopy pairs
wav_exts = {".wav"}          # add more if needed
mfcc_ext = ".mfcc"           # or ".mfc"
# -------------------------------

def is_ignored(p: Path) -> bool:
    return any(part == ".ipynb_checkpoints" for part in p.parts)

pairs = []
for wav in sorted(data_dir.rglob("*")):
    if wav.is_file() and wav.suffix.lower() in wav_exts and not is_ignored(wav):
        # write MFCC right next to the WAV (same folder, different extension)
        mfc_path = wav.with_suffix(mfcc_ext)
        pairs.append(f"{wav.as_posix()}\t{mfc_path.as_posix()}\n")

if not pairs:
    raise SystemExit(f"No WAV files found under {data_dir}")

out_scp.write_text("".join(pairs), encoding="utf-8")
print(f"Wrote {len(pairs)} entries to {out_scp}")
