import os

# ~/Programming/Datascience/ING/PZR/htk/fun $ ../../../../.venv/bin/python ./helper_scripts/generate_trainscp.py
DATA_DIR = "data"
PARAM_LIST = "param.list"

# Open once in append mode (creates it if it doesn't exist)
with open(PARAM_LIST, "a") as f:
    # Walk through each subfolder under data/
    for person_folder in os.listdir(DATA_DIR):
        person_path = os.path.join(DATA_DIR, person_folder)
        if not os.path.isdir(person_path):
            continue

        # For every .wav file in that folder, append one line
        for fname in os.listdir(person_path):
            if not fname.lower().endswith(".wav"):
                continue
            wav_path = os.path.join(person_path, fname)
            mfcc_path = wav_path.rsplit(".", 1)[0] + ".mfcc"
            f.write(f"{wav_path}\t{mfcc_path}\n")

print(f"✅ Updated: {PARAM_LIST}")
