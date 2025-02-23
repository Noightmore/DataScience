#!/bin/bash

# Set the target directory
RECORDINGS_DIR="./p2501"

# Check if the directory exists
if [ ! -d "$RECORDINGS_DIR" ]; then
    echo "❌ The folder '$RECORDINGS_DIR' does not exist!"
    exit 1
fi

# Enable nullglob to avoid errors if no .opus files exist
shopt -s nullglob

# Find all .opus files in the recordings folder
files=("$RECORDINGS_DIR"/*.wav)

# Check if there are any .opus files
if [ ${#files[@]} -eq 0 ]; then
    echo "❌ No .wav files found in '$RECORDINGS_DIR'!"
    exit 1
fi

echo "🎵 Playing all .wav recordings from '$RECORDINGS_DIR'..."
sleep 1

# Loop through and play each file
for file in "${files[@]}"; do
    echo -e "\n▶️ Playing: $file"
    ffplay -autoexit -nodisp "$file"
done

echo "✅ All recordings played!"
