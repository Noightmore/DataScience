#!/usr/bin/env python3
import os

# Define the base directories and their corresponding folder lists.
# Each tuple is (base_path, [list_of_subfolders]).
base_folders = [
    # 2021
    ("cislovky-2021/2021", [
        "p2101", "p2102", "p2103", "p2104", "p2105", "p2106",
        "p2109", "p2110", "p2111", "p2112"
    ]),
    # 2022
    ("cislovky-2022/2022", [
        "p2201", "p2202", "p2203", "p2204", "p2206", "p2207"
    ]),
    # 2023
    ("cislovky-2023/2023", [
        "p2301", "p2302", "p2303", "p2304", "p2305", "p2306",
        "p2307", "p2308"
    ]),
    # 2024
    ("cislovky-2024/2024", [
        "p2401", "p2402", "p2404", "p2405"
    ]),
    # 2025
    ("cislovky-2025/2025", [
        "p2501", "p2502", "p2503", "p2504"
    ])
]

# Ranges for 'c' (0..9) and 's' (01..05)
c_values = range(10)      # c0..c9
s_values = range(1, 6)    # s01..s05

for base_path, folders in base_folders:
    for folder in folders:
        # Create a file list name, e.g. "FileList_p2101.txt"
        output_filename = f"FileList_{folder}.txt"

        with open(output_filename, "w") as f:
            # For each s (01..05), then each c (0..9)
            for s in s_values:
                for c in c_values:
                    # Construct the WAV filename (e.g. c0_p2101_s01.wav)
                    file_name = f"c{c}_{folder}_s{str(s).zfill(2)}.wav"

                    # Construct the full path (base_path/folder/filename)
                    full_path = os.path.join(base_path, folder, file_name)

                    # Write the path to the output file
                    f.write(full_path + "\n")

        print(f"Generated file list: {output_filename}")
