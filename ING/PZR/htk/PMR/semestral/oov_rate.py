from pathlib import Path

def load_wordlist(path: Path) -> set[str]:
    words = set()
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            w = line.strip()
            if not w or w.startswith("#"):
                continue
            # allow "WORD phone phone ..." or just "WORD"
            w = w.split()[0]
            words.add(w)
    return words

def iter_mlf_labels(mlf_path: Path):
    with mlf_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#!MLF!#"):
                continue
            if s.startswith('"') and s.endswith('"'):
                continue
            if s == ".":
                continue
            # accept either:
            #   word
            # or: start end word [score]
            parts = s.split()
            yield parts[-1] if len(parts) >= 3 and parts[0].isdigit() else parts[0]

def oov_rate_for_wordlist(wordlist_path: Path, ref_mlf_path: Path):
    wl = load_wordlist(wordlist_path)
    oov = 0
    total = 0
    for lab in iter_mlf_labels(ref_mlf_path):
        total += 1
        if lab not in wl:
            oov += 1
    rate = (oov / total) if total else 0.0
    return oov, total, rate

# --- usage (edit these) ---
ref_mlf = Path("semestral/test_phones_0-100.mlf")
wordlists = [
    Path("semestral/wlists_mlfs/wlist_top10000.wlist"),
    Path("semestral/wlists_mlfs/wlist_top60000.wlist"),
    Path("semestral/wlists_mlfs/wlist_top20000.wlist")
]


if __name__ == "__main__":
    print(f"{'wordlist':45s}  {'OOV':>8s}  {'Total':>8s}  {'OOV%':>8s}")
    print("-" * 75)
    for wl_path in wordlists:
        oov, total, rate = oov_rate_for_wordlist(wl_path, ref_mlf)
        print(f"{str(wl_path):45s}  {oov:8d}  {total:8d}  {rate*100:7.2f}")

"""
wordlist                                            OOV     Total      OOV%
---------------------------------------------------------------------------
semestral/wlists_mlfs/wlist_top10000.wlist          428      1882    22.74
semestral/wlists_mlfs/wlist_top60000.wlist          104      1882     5.53
semestral/wlists_mlfs/wlist_top20000.wlist          272      1882    14.45
"""