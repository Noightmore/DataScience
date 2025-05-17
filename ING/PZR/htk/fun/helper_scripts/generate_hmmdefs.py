import os
import shutil

#

# Settings
work_dir = "."  # Update this! !!!!!!!!!!!!!!!!!
proto_8s = os.path.join(work_dir, "proto-8s-39f")
proto_3s = os.path.join(work_dir, "proto-3s-39f")
models_list = os.path.join(work_dir, "models0")

# Define short words (3-state)
short_words = {"V", "ZA", "SIL"} # remove unnecessary short phrases, ok

# Load prototypes
with open(proto_8s, "r") as f:
    proto8_content = f.read()

with open(proto_3s, "r") as f:
    proto3_content = f.read()

# Generate hmm0/hmmdefs
hmm0_dir = os.path.join(work_dir, "hmm0")
os.makedirs(hmm0_dir, exist_ok=True)
output_hmmdefs = os.path.join(hmm0_dir, "hmmdefs")

with open(models_list, "r") as models, open(output_hmmdefs, "w") as hmmdefs:
    for model_name in models:
        model_name = model_name.strip()
        if model_name == "":
            continue
        # Select prototype
        if model_name.lower() in short_words:
            hmm_content = proto3_content.replace('~h "proto-3s-39f"', f'~h "{model_name}"')
        else:
            hmm_content = proto8_content.replace('~h "proto-8s-39f"', f'~h "{model_name}"')

        hmmdefs.write(hmm_content + "\n")

print(f"✅ Generated hmm0/hmmdefs")

# Copy hmm0 → hmm1 ... hmm5
for i in range(1, 6):
    hmm_dir = os.path.join(work_dir, f"hmm{i}")
    os.makedirs(hmm_dir, exist_ok=True)
    shutil.copy(output_hmmdefs, os.path.join(hmm_dir, "hmmdefs"))
    print(f"✅ Copied hmm0/hmmdefs → hmm{i}/hmmdefs")

print("🎯 All hmmdefs generated and copied!")
