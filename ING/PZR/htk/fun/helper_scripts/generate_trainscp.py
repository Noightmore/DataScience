import os

# ~/Programming/Datascience/ING/PZR/htk/fun $ ../../../../.venv/bin/python ./helper_scripts/generate_trainscp.py

DATA_DIR = "data"

for person_folder in os.listdir(DATA_DIR):
    person_path = os.path.join(DATA_DIR, person_folder)
    if not os.path.isdir(person_path):
        continue  # skip if not a folder

    scp_path = os.path.join("train.scp")
    with open(scp_path, "w") as f:
        for file in os.listdir(person_path):
            if file.endswith(".mfcc"):
                mfcc_path = os.path.join(person_path, file)
                f.write(f"{mfcc_path}\n")

    print(f"✅ Created: {scp_path}")
