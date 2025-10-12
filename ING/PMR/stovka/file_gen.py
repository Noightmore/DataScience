import os
import re
from datetime import datetime
from typing import Callable, Dict
import unicodedata as ud

def _sanitize_filename(text: str) -> str:
    # Normalize Unicode and strip diacritics (e.g. ř -> r, č -> c, ě -> e)
    def remove_diacritics(s: str) -> str:
        return ''.join(
            c for c in ud.normalize('NFD', s)
            if ud.category(c) != 'Mn'
        )

    base = text.strip().lower()
    base = remove_diacritics(base)
    base = re.sub(r'\s+', '_', base)
    # remove . ,!?;:„“"\'()\-–— and other punctuation at the end
    base = re.sub(r'[.,!?;:„“"\'()\-–—]+$', '', base)
    base = base[:60] if base else "recording"
    return f"{base}.wav"

# --- mapping: (second column) -> (third column) ---
PHONEME_MAP: Dict[str, str] = {
    "a": "a",
    "á": "aa",
    "b": "b",
    "c": "ts",
    "C": "dz",
    "č": "ch",
    "Č": "dg",
    "d": "d",
    "ď": "dj",
    "e": "e",
    "é": "ee",
    "f": "f",
    "g": "g",
    "h": "h",
    "X": "x",
    "i": "i",
    "í": "ii",
    "j": "y",
    "k": "k",
    "l": "l",
    "m": "m",
    "M": "mg",
    "n": "n",
    "N": "ng",
    "ň": "nj",
    "o": "o",
    "ó": "oo",
    "p": "p",
    "r": "r",
    "ř": "rz",
    "Ř": "rs",
    "s": "s",
    "š": "sh",
    "t": "t",
    "ť": "tj",
    "u": "u",
    "ú": "uu",
    "v": "v",
    "z": "z",
    "ž": "zh",
    "-": "si",
    "E": "swa",
    "1": "n1",
    "2": "n2",
    "3": "n3",
    "4": "n4",
    "5": "n5",
    "0": "n0",
}

def generate_files(
        sentence: str,
        output_dir: str,
        rewrite_text: Callable[[str], str],
) -> dict:
    """
    Create:
      - <stem>.txt  (CP1250)  -> original sentence
      - <stem>.phn  (UTF-8)   -> rewrite_text(sentence with all whitespace removed)
      - <stem>.lab  (UTF-8)   -> per-char mapping from .phn: '0 0 <mapped>' per line

    Returns dict with paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    wav_name = _sanitize_filename(sentence)
    stem = os.path.splitext(wav_name)[0]

    txt_path = os.path.join(output_dir, f"{stem}.txt")
    phn_path = os.path.join(output_dir, f"{stem}.phn")
    lab_path = os.path.join(output_dir, f"{stem}.lab")

    encoding_type = "utf-8" # "cp1250"

    # 1) .txt in CP1250
    with open(txt_path, "w", encoding="cp1250", errors="replace") as f_txt:
        f_txt.write(sentence)

    # 2) .phn from whitespace-stripped sentence
    no_ws = re.sub(r"\s+", "", sentence)
    # remove punctuation, hyphens, colons, semicolons, quotes, etc.
    no_ws = re.sub(r"[.,!?;:„“\"'()\-–—]", "", no_ws)

    phn_str = rewrite_text(no_ws)
    # Store exactly as returned (trim trailing newlines once)
    phn_str = phn_str.rstrip("\n")

    with open(phn_path, "w", encoding=encoding_type) as f_phn:
        f_phn.write(phn_str + "\n")

    # 3) .lab: iterate chars of phn_str, map via PHONEME_MAP, one per line
    with open(lab_path, "w", encoding=encoding_type) as f_lab:
        for idx, ch in enumerate(phn_str):
            try:
                mapped = PHONEME_MAP[ch]
            except KeyError:
                raise ValueError(
                    f"Character at position {idx} in .phn ('{ch}') "
                    f"has no mapping in PHONEME_MAP."
                )
            f_lab.write(f"0 0 {mapped}\n")

    return {
        "txt": txt_path,
        "phn": phn_path,
        "lab": lab_path,
        "stem": stem,
        "wav_name": wav_name,
    }

if __name__ == "__main__":
    # Example dummy rewrite_text function
    # In your real setup, this should convert Czech text into phoneme symbols

    from ING.PMR.antlr_fun.fun import rewrite_text

    sentence = "Společnost dělá řád."

    print(f"Generating files for: {sentence}")

    paths = generate_files(
        sentence=sentence,
        output_dir="out",  # Folder for generated files
        rewrite_text=rewrite_text
    )

    print("\nGenerated files:")
    for key, value in paths.items():
        print(f"  {key}: {value}")

    # Preview file contents
    print("\n--- .phn content ---")
    with open(paths["phn"], "r", encoding="utf-8") as f:
        print(f.read())

    print("--- .lab content ---")
    with open(paths["lab"], "r", encoding="utf-8") as f:
        print(f.read())
