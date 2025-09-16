import os

# ~/Programming/Datascience/ING/PZR/htk/fun $ ../../../../.venv/bin/python ./helper_scripts/generate_trainscp.py

DATA_DIR = "data"
SCP_FILE = "train.scp"

# 1) Read any existing entries so we don’t duplicate
seen = set()
if os.path.exists(SCP_FILE):
    with open(SCP_FILE, "r") as f:
        for line in f:
            seen.add(line.strip())

# 2) Open once in append mode and add only new paths
with open(SCP_FILE, "a") as f:
    for person_folder in os.listdir(DATA_DIR):
        person_path = os.path.join(DATA_DIR, person_folder)
        if not os.path.isdir(person_path):
            continue

        for fname in os.listdir(person_path):
            if not fname.lower().endswith(".mfcc"):
                continue

            full_path = os.path.join(person_path, fname)
            if full_path not in seen:
                f.write(full_path + "\n")
                seen.add(full_path)

print(f"✅ Updated (appended new entries): {SCP_FILE}")

