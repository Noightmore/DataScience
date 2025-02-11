#!/bin/bash

MIC="hw:2,0"  # Set your microphone input; it is different for each machine
RECORDINGS_DIR="./recordings"  # Target directory for recordings

# Create the recordings folder if it doesn't exist
mkdir -p "$RECORDINGS_DIR"

# List of phrases to record
files=("je_prave" "hodina" "hodin" "hodiny" "minuta" "minut" "minuty" "1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "30" "40" "50")

# Function to play a beep sound
beep_sound() {
    echo -e '\a'  # Built-in terminal beep (if enabled)
}

for file in "${files[@]}"; do
    echo -e "\nPress ENTER to start recording: $file"
    read -r  # Wait for ENTER key

    beep_sound  # Beep before recording
    echo "Recording: $file... Press ENTER to stop."

    # Start recording in the background and save in the recordings folder
    ffmpeg -f alsa -i "$MIC" -c:a libopus -b:a 24k -ar 16000 -ac 1 "$RECORDINGS_DIR/$file.opus" &
    RECORD_PID=$!  # Store the process ID of FFmpeg

    read -r  # Wait for ENTER key to stop
    kill "$RECORD_PID"  # Stop the recording

    beep_sound  # Beep after recording
    echo "✅ Saved: $RECORDINGS_DIR/$file.opus"
    sleep 1  # Small pause before the next recording
done

echo "🎤 ✅ All recordings completed and saved in '$RECORDINGS_DIR'!"
