from pathlib import Path

mfcc_lst = Path("mfcc/mfcc.lst")
prot_lst = Path("prot/prot.lst")
prot_lst.parent.mkdir(parents=True, exist_ok=True)

out = []
for i, line in enumerate(mfcc_lst.read_text(encoding="utf-8").splitlines(), 1):
    if not line.strip():
        continue
    # accept tabs or multiple spaces
    parts = line.strip().split()
    if len(parts) < 2:
        raise ValueError(f"Line {i} has no 2nd column: {line!r}")
    out.append(parts[1])

# (optional) de-dup and keep order
seen = set()
unique = [p for p in out if not (p in seen or seen.add(p))]
2
prot_lst.write_text("\n".join(unique) + "\n", encoding="utf-8")
print(f"Wrote {len(unique)} entries to {prot_lst}")
