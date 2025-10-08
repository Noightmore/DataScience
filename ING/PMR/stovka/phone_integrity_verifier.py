import unicodedata as ud
from collections import Counter, defaultdict
from typing import List, Tuple, Dict

def normalize_text(s: str) -> str:
    return ud.normalize("NFC", s).lower()

def verify_phonemes(sentences: List[str], min_count: int = 3) -> Tuple[bool, Dict[str,int], Dict[str,int]]:
    """
    Verify that all PAC phonemes (represented by orthographic graphemes)
    appear at least min_count times in the provided sentences.

    Returns:
      ok (bool) - True if every target phoneme count >= min_count
      counts (dict) - mapping phoneme_key -> total count found
      details (dict) - helpful breakdown of matched graphemes per phoneme
    """
    # PAC phoneme keys mapped to orthographic grapheme lists (based on PDF table)
    # Digraphs must be matched before single letters -> put them separately / counted first.
    phoneme_map = {
        'a': ['a'],
        'á': ['á'],
        'b': ['b'],
        'c': ['c'],
        'dz': ['dz'],     # PAC symbol C
        'č': ['č'],
        'dž': ['dž'],     # PAC symbol Č
        'd': ['d'],
        'ď': ['ď'],
        'e': ['e'],
        'é': ['é'],
        'f': ['f'],
        'g': ['g'],
        'h': ['h'],
        'ch': ['ch'],     # PAC symbol X
        # i / y -> PAC single phoneme
        'i': ['i', 'y'],
        'í': ['í', 'ý'],
        'j': ['j'],
        'k': ['k'],
        'l': ['l'],
        'm': ['m'],
        'n': ['n'],
        'ň': ['ň'],
        'o': ['o'],
        'ó': ['ó'],
        'p': ['p'],
        'r': ['r'],
        'ř': ['ř'],       # lowercase only (we normalize)
        's': ['s'],
        'š': ['š'],
        't': ['t'],
        'ť': ['ť'],
        'u': ['u'],
        'ú': ['ú', 'ů'],  # ú and ů are same phoneme in PAC
        'v': ['v'],
        'z': ['z'],
        'ž': ['ž'],
    }

    # Order digraphs first so they don't get double-counted as single letters
    digraph_order = ['dž', 'dz', 'ch']

    # accumulator for counts and details
    counts = {k: 0 for k in phoneme_map.keys()}
    details = {k: Counter() for k in phoneme_map.keys()}

    # combine sentences into one list of normalized strings
    normalized = [normalize_text(s) for s in sentences]

    # For each sentence: first count digraphs (remove them), then count remaining single chars/aliases
    for s in normalized:
        working = s
        # count digraph occurrences and remove them from the working string (replace with space)
        for dg in digraph_order:
            if dg in working:
                n = working.count(dg)
                counts[dg] += n
                details[dg][dg] += n
                # remove all occurrences so 'd' and 'z' are not double counted from 'dz'
                working = working.replace(dg, ' ')

        # now count single-letter graphemes (including aliases)
        # We go phoneme by phoneme and sum up occurrences of listed graphemes
        for ph, graphemes in phoneme_map.items():
            # skip digraph keys (already handled)
            if ph in digraph_order:
                continue
            total_here = 0
            for g in graphemes:
                # count direct occurrences
                n = working.count(g)
                if n:
                    total_here += n
                    details[ph][g] += n
                    # remove so that overlapping matches are not recounted
                    working = working.replace(g, ' ')
            counts[ph] += total_here

    # Now aggregate counts: ensure keys exist for digraphs too (they are in counts already)
    # Check which phonemes are below min_count
    missing = {ph: cnt for ph, cnt in counts.items() if cnt < min_count}

    ok = (len(missing) == 0)
    return ok, counts, details

# Example usage:
if __name__ == "__main__":
    # sentences = [...]  # put your list of Czech sentences here
    # ok, counts, details = verify_phonemes(sentences, min_count=3)
    # print("All phonemes >=3? ", ok)
    # print("Counts:", counts)
    # print("Missing / underrepresented:", {k:v for k,v in counts.items() if v < 3})
    pass
