#!/usr/bin/env python3
import os
import wave
import contextlib

def get_wav_duration(filepath):
    """Return duration of a WAV file in seconds."""
    try:
        with contextlib.closing(wave.open(filepath, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / float(rate)
    except Exception:
        return 0.0

def get_leaf_dirs(root):
    """Return all leaf directories (those without subdirectories)."""
    leaf_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        if not dirnames:  # no subdirectories
            leaf_dirs.append(dirpath)
    return leaf_dirs

def calculate_stats(base_dir, exclude_test=False):
    total_seconds = 0.0
    total_wavs = 0
    persons = 0

    for folder in get_leaf_dirs(base_dir):
        # Skip folders under data/Test if excluding test set
        if exclude_test and os.path.abspath("data/Test") in os.path.abspath(folder):
            continue

        wav_files = [f for f in os.listdir(folder) if f.lower().endswith(".wav")]
        if not wav_files:
            continue  # skip empty folders

        persons += 1
        total_wavs += len(wav_files)

        for wav in wav_files:
            path = os.path.join(folder, wav)
            total_seconds += get_wav_duration(path)

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    return persons, total_wavs, hours, minutes, seconds

def print_stats(label, persons, total_wavs, hours, minutes, seconds):
    print(f"=== {label} DATA ===")
    print(f"Unique persons (leaf folders): {persons}")
    print(f"Total WAV files:               {total_wavs}")
    print(f"Total duration:                {hours}h {minutes}m {seconds}s\n")

if __name__ == "__main__":
    if not os.path.isdir("data"):
        print("Error: 'data' folder not found!")
        exit(1)

    # Training: everything except data/Test
    persons, wavs, h, m, s = calculate_stats("data", exclude_test=True)
    print_stats("TRAINING (excluding Test)", persons, wavs, h, m, s)

    # Testing: only inside data/Test
    if os.path.isdir("data/Test") or os.path.isdir("data/Test2") or os.path.isdir("data/Test3"):
        persons, wavs, h, m, s = calculate_stats("data/Test", exclude_test=False)
        print_stats("TESTING", persons, wavs, h, m, s)
    else:
        print("No data/Test folder found — skipping test stats.")
