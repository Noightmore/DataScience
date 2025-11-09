from pathlib import Path
import re
import sys

# === Configuration ===
root = Path(".")
in_dir = root / "Spojovatelka"   # folder with .lab files
backup_ext = ".bak"
encoding = "cp1250"

# --- Allowed words (lowercase, no diacritics) ---
ALLOWED = {
    "si",
    "spojte", "mi",
    "chtel", "bych",
    "prosim",
    "dejte",
    "bozenu", "cernou",
    "evu", "dvorakovou",
    "adama", "novaka",
    "petra", "svobodu",
    "jiriho", "maleho",
    "veru", "pokornou",
}

def ok_core(tokens):
    """Return True if tokens form a valid 3- or 4-word pattern according to grammar."""
    if len(tokens) == 4:
        a,b,c,d = tokens
        if a == "spojte" and b == "mi": return True
        if a == "chtel" and b == "bych": return True
        if a == "dejte" and b == "mi": return True
        # prosim case could also produce 4-word (rare), still valid
        if a == "prosim": return True
    elif len(tokens) == 3:
        a,b,c = tokens
        if a == "prosim": return True
    return False

if __name__ == "__main__":
    if not in_dir.exists():
        sys.exit(f"Folder not found: {in_dir}")

    labs = sorted(in_dir.rglob("*.lab"))
    if not labs:
        sys.exit(f"No .lab files found in {in_dir}")

    done, bad = 0, []

    for lab_path in labs:
        stem = lab_path.stem.lower()
        cleaned = re.sub(r"[^a-z0-9_]", "", stem)
        tokens = [t for t in cleaned.split("_") if t]

        # remove any trailing non-allowed suffixes (e.g. z01)
        while tokens and tokens[-1] not in ALLOWED:
            tokens.pop()

        if not tokens or not all(t in ALLOWED for t in tokens) or not ok_core(tokens):
            bad.append((lab_path.name, tokens))
            continue

        # --- build new label content ---
        out_lines = ["si", *tokens, "si", ""]
        new_text = "\n".join(out_lines)

        # backup old file
        bak = lab_path.with_suffix(lab_path.suffix + backup_ext)
        try:
            if not bak.exists():
                bak.write_text(lab_path.read_text(encoding=encoding), encoding=encoding)
        except Exception:
            pass  # ignore unreadable files

        # overwrite with new word-level labels
        lab_path.write_text(new_text, encoding=encoding)
        done += 1

    print(f"✅ Rewritten {done} .lab files in '{in_dir}'.")
    if bad:
        print("⚠ Skipped files (name not matching grammar):")
        for name, toks in bad[:20]:
            print(f" - {name}: tokens={toks}")
        if len(bad) > 20:
            print(f"  ... and {len(bad)-20} more")
