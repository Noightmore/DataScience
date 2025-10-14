#!/bin/bash
# Fix missing "-" in .phn files and add "0 0 si" lines in .lab files
cd ./recordings
shopt -s nullglob

# --- Fix all .phn files ---
for f in *.phn; do
  echo "Processing PHN: $f"

  # Read first line (trim newlines)
  firstline=$(head -n 1 "$f" | tr -d '\r\n')

  # Check and fix missing leading/trailing '-'
  if [[ $firstline != -* ]]; then
    firstline="-$firstline"
  fi
  if [[ $firstline != *- ]]; then
    firstline="${firstline}-"
  fi

  # Overwrite with corrected line (keep single line only)
  echo "$firstline" > "$f"
done

# --- Fix all .lab files ---
for f in *.lab; do
  echo "Processing LAB: $f"

  tmpfile=$(mktemp)

  # read all content
  mapfile -t lines < "$f"

  # add first "0 0 si" if missing
  if [[ "${lines[0]}" != "0 0 si" ]]; then
    echo "0 0 si" > "$tmpfile"
  fi

  # write original lines
  printf "%s\n" "${lines[@]}" >> "$tmpfile"

  # add last "0 0 si" if missing
  last="${lines[-1]}"
  if [[ "$last" != "0 0 si" ]]; then
    echo "0 0 si" >> "$tmpfile"
  fi

  # replace original file
  mv "$tmpfile" "$f"
done

echo "All .phn and .lab files have been fixed."
