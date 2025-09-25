#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 path/to/your.wav" >&2
  exit 1
fi

INPUT_WAV=$1

# 1) Convert wav → temporary MFCC
TMPMFC=$(mktemp /tmp/htk.XXXXXX.mfc)
HCopy -C ParamConfig -T 1 "$INPUT_WAV" "$TMPMFC"

# 2) Prepare a one‐line scp for HVite
TMPSCP=$(mktemp /tmp/htk.XXXXXX.scp)
echo "$TMPMFC" > "$TMPSCP"

# 3) Decode into a temporary MLF
RECMFL=$(mktemp /tmp/htk.XXXXXX.mlf)
HVite -T 1 \
      -C TrainConfig \
      -H hmm6/hmmdefs \
      -S "$TMPSCP" \
      -i "$RECMFL" \
      -w wordnet \
      dict models0 

# 4) Extract the recognized words from the MLF
#    Skip the header line, the utterance‐name lines, and the single “.”
awk '
  /^#!MLF/    { next }      # skip header
  /^"/       { next }      # skip utterance-name lines
  /^\.$/     { next }      # skip the lone dot
  { printf "%s ", $1 }     # print each word
END { print "" }
' "$RECMFL"

# 5) Clean up
rm -f "$TMPMFC" "$TMPSCP" "$RECMFL"
