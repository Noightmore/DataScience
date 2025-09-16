import os

#  ~/Programming/Datascience/ING/PZR/htk/fun $ ../../../../.venv/bin/python ./helper_scripts/generate_lab_files.py

DATA_DIR = "data"
SIL = "sil"

for person_folder in os.listdir(DATA_DIR):
    person_path = os.path.join(DATA_DIR, person_folder)
    if not os.path.isdir(person_path):
        continue  # skip non-folders

    for file in os.listdir(person_path):
        if file.endswith(".wav") and file.startswith("w"):
            base_name = os.path.splitext(file)[0]
            word = base_name.split("_")[0][1:]  # extract part after 'w' and before '_'
            word = word.lower()
            lab_path = os.path.join(person_path, f"{base_name}.lab")

            with open(lab_path, "w") as f:
                f.write(SIL+"\n")
                f.write(f"{word}\n")
                f.write(SIL+"\n")

            print(f"✅ Created: {lab_path} with word: {word}")
