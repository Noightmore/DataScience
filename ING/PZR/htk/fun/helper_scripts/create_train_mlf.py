import os

DATA_DIR = "data"
MLF_FILE = "train.mlf"

with open(MLF_FILE, "w") as mlf:
    mlf.write("#!MLF!#\n")
    for person_folder in os.listdir(DATA_DIR):
        person_path = os.path.join(DATA_DIR, person_folder)
        if not os.path.isdir(person_path):
            continue  # Skip non-folders

        for file in os.listdir(person_path):
            if file.endswith(".lab"):
                lab_path = os.path.join(person_path, file)
                relative_lab_path = lab_path  # Keep relative path

                mlf.write(f"\"{relative_lab_path}\"\n")

                with open(lab_path, "r") as lab_file:
                    for line in lab_file:
                        mlf.write(line)
                mlf.write(".\n")

print(f"✅ Created {MLF_FILE}")
