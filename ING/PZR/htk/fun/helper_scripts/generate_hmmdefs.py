import os
import shutil

# Settings
work_dir = "."  # Update this as needed
proto_8s = os.path.join(work_dir, "proto-8s-39f")
proto_3s = os.path.join(work_dir, "proto-3s-39f")
models_list = os.path.join(work_dir, "models0")

# Define short words (3-state)
short_words = {"SIL", "DNU", "HODIN"}  # uppercase names for consistency

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
        if not model_name:
            continue
        # always use uppercase for HMM names
        name_upper = model_name.upper()
        # Select prototype
        if name_upper in short_words:
            name_upper = name_upper.lower()    
            hmm_content = proto3_content.replace('~h "proto-3s-39f"', f'~h "{name_upper}"')
        else:
            name_upper = name_upper.lower()
            hmm_content = proto8_content.replace('~h "proto-8s-39f"', f'~h "{name_upper}"')

        hmmdefs.write(hmm_content + "\n")

print(f"✅ Generated {output_hmmdefs}")

# Copy hmm0 → hmm1 ... hmm5
for i in range(1, 6):
    src = output_hmmdefs
    dst_dir = os.path.join(work_dir, f"hmm{i}")
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copy(src, os.path.join(dst_dir, "hmmdefs"))
    print(f"✅ Copied {src} → {dst_dir}/hmmdefs")

print("🎯 All hmmdefs generated and copied!")

