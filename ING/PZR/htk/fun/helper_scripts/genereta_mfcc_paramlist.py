import os

# ~/Programming/Datascience/ING/PZR/htk/fun $ ../../../../.venv/bin/python ./helper_scripts/generate_trainscp.py

DATA_DIR = "data"

for person_folder in os.listdir(DATA_DIR):
    person_path = os.path.join(DATA_DIR, person_folder)
    if not os.path.isdir(person_path):
        continue  # skip files, only process folders

    param_list_path = os.path.join("param.list")
    with open(param_list_path, "w") as f:
        for file in os.listdir(person_path):
            if file.endswith(".wav"):
                wav_path = os.path.join(person_path, file)
                mfcc_path = wav_path.replace(".wav", ".mfcc")
                f.write(f"{wav_path}\t{mfcc_path}\n")

    print(f"✅ Created: {param_list_path}")
