from pathlib import Path

# ---- settings ----
data_dir = Path("data")         # root containing all .lab files (nested subfolders ok)
out_dir  = Path(".")            # where to write the MLFs
train_mlf = out_dir / "train_phones.mlf"
test_mlf  = out_dir / "test_phones.mlf"
test_root = data_dir / "Test"   # EXACT subtree that should go to test
lab_encoding = "cp1250"         # your .lab files are CP1250
# -------------------

out_dir.mkdir(parents=True, exist_ok=True)

def is_ignored(path: Path) -> bool:
    # ignore any file under a .ipynb_checkpoints directory
    return any(part == ".ipynb_checkpoints" for part in path.parts)

# collect all .lab files under data/, recursively, excluding .ipynb_checkpoints
all_labs = sorted(
    p for p in data_dir.rglob("*.lab")
    if p.is_file() and not is_ignored(p)
)
if not all_labs:
    raise SystemExit(f"No .lab files found under {data_dir.resolve()}")

def is_under(path: Path, root: Path) -> bool:
    """True if 'path' is inside 'root' (including root itself)."""
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False

# split STRICTLY by data/Test subtree
test_labs  = [p for p in all_labs if is_under(p, test_root)]
train_labs = [p for p in all_labs if not is_under(p, test_root)]

print(f"Found {len(train_labs)} train and {len(test_labs)} test .lab files.")
print(f" test root: {test_root.as_posix()}")

def label_target_line(lab_path: Path) -> str:
    """
    Build the quoted target label name starting at 'data/'.
    Example: "data/spk01/sessionA/utt001.lab"
    """
    rel = lab_path.relative_to(data_dir)            # spk01/sessionA/utt001.lab
    full = (data_dir / rel).as_posix()             # data/spk01/sessionA/utt001.lab
    return f"\"{full}\"\n"

def write_mlf(paths, out_path: Path):
    lines = ["#!MLF!#\n"]
    for lab in paths:
        lines.append(label_target_line(lab))
        # read label file as CP1250 (safer for your files)
        txt = lab.read_text(encoding=lab_encoding, errors="strict")
        if not txt.endswith("\n"):
            txt += "\n"
        lines.append(txt)
        lines.append(".\n")
    out_path.write_text("".join(lines), encoding="utf-8")  # MLF can be UTF-8
    print(f"Wrote {len(paths)} utterances → {out_path}")

write_mlf(train_labs, train_mlf)
write_mlf(test_labs,  test_mlf)
