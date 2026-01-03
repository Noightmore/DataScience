#!/usr/bin/env python3
import argparse
import re
import unicodedata
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from antlr_fun.fun import rewrite_text


# ----------------- text utils -----------------

def strip_diacritics(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def normalize_for_similarity(s: str) -> str:
    # compare on diacritics-stripped lowercase alnum only
    s = strip_diacritics(s).lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    if len(b) > len(a):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            ins = cur[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + (ca != cb)
            cur.append(min(ins, dele, sub))
        prev = cur
    return prev[-1]


# ----------------- dict loading -----------------

def load_pseudo_to_labels(dict_path: Path, encoding: str) -> Dict[str, List[str]]:
    """
    Dict format: COL1=label, COL2=pseudo(key). Extra columns ignored.
    Stores: pseudo -> [label1, label2, ...]
    """
    pseudo2labels: Dict[str, List[str]] = {}
    with dict_path.open("r", encoding=encoding, errors="strict") as f:
        for ln_no, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                raise ValueError(f"{dict_path}:{ln_no}: expected >=2 columns, got: {line!r}")
            label = parts[0]
            pseudo = parts[1]
            pseudo2labels.setdefault(pseudo, []).append(label)
    return pseudo2labels


def pick_best_label(labels: List[str], original_word: str) -> Tuple[str, bool]:
    """
    If multiple labels for same pseudo, pick the label closest to original word
    (diacritics stripped). Returns (chosen_label, had_collision).
    """
    if len(labels) == 1:
        return labels[0], False

    target = normalize_for_similarity(original_word)
    best = labels[0]
    best_score = float("inf")

    for lab in labels:
        score = levenshtein(target, normalize_for_similarity(lab))
        if score < best_score:
            best_score = score
            best = lab

    return best, True


# ----------------- corpus tokenization -----------------

# Remove common sentence punctuation. Keep letters, digits, diacritics in tokens.
TOKEN_RE = re.compile(r"[0-9A-Za-zÀ-ž]+")


def iter_corpus_tokens(corpus_path: Path, encoding: str) -> Iterable[str]:
    """
    Corpus may be sentences per line or multiple sentences per line.
    We extract word tokens by regex, effectively stripping . , ? ! etc.
    """
    with corpus_path.open("r", encoding=encoding, errors="strict") as f:
        for line in f:
            for tok in TOKEN_RE.findall(line):
                yield tok


# ----------------- main -----------------

def main():
    ap = argparse.ArgumentParser(
        description=(
            "Build HTK .lab files from a text corpus.\n"
            "Dictionary: COL1=label, COL2=pseudo(key).\n"
            "Corpus: sentences per line or multiple sentences per line; tokens extracted and punctuation .,!?: removed.\n"
            "For each token: pseudo=rewrite_text(token) -> label lookup -> output chosen label lowercased.\n"
            "Writes N tokens per .lab file, files named 0.lab, 1.lab, ...\n"
        )
    )
    ap.add_argument("--dict", dest="dict_path", type=Path, required=True)
    ap.add_argument("--corpus", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)

    ap.add_argument("--dict-encoding", default="utf-8")
    ap.add_argument("--corpus-encoding", default="cp1250")
    ap.add_argument("--out-encoding", default="utf-8")

    ap.add_argument("--tokens-per-lab", type=int, default=10,
                    help="How many corpus tokens per .lab file (default: 10).")
    ap.add_argument("--limit", type=int, default=0,
                    help="Stop after N tokens processed (0 = no limit).")

    ap.add_argument("--report-collisions", type=int, default=200,
                    help="Print up to N collision resolutions (default: 200).")
    ap.add_argument("--oov-policy", choices=["skip", "error"], default="skip",
                    help="If pseudo not in dict: skip token or raise error (default: skip).")

    args = ap.parse_args()

    pseudo2labels = load_pseudo_to_labels(args.dict_path, args.dict_encoding)
    print(f"[dict] loaded pseudos={len(pseudo2labels)}")

    args.out.mkdir(parents=True, exist_ok=True)

    file_index = 0
    in_file = 0
    buf: List[str] = []

    processed = 0
    files_written = 0
    oov_skipped = 0
    collisions = 0
    collisions_reported = 0

    def flush():
        nonlocal file_index, in_file, buf, files_written
        if not buf:
            return
        out_path = args.out / f"{file_index}.lab"
        out_path.write_text("\n".join(buf) + "\n", encoding=args.out_encoding)
        file_index += 1
        in_file = 0
        buf = []
        files_written += 1

    for tok in iter_corpus_tokens(args.corpus, args.corpus_encoding):
        processed += 1
        if args.limit and processed > args.limit:
            break

        pseudo = rewrite_text(tok)
        labels = pseudo2labels.get(pseudo)

        if labels is None:
            oov_skipped += 1
            if args.oov_policy == "error":
                raise KeyError(f"OOV token={tok!r} pseudo={pseudo!r}")
            continue

        chosen, had_collision = pick_best_label(labels, tok)

        if had_collision:
            collisions += 1
            if collisions_reported < args.report_collisions:
                target = normalize_for_similarity(tok)
                scored = sorted(
                    [(levenshtein(target, normalize_for_similarity(lab)), lab) for lab in labels],
                    key=lambda x: x[0]
                )
                print(
                    f"[COLLISION] token={tok!r} pseudo={pseudo!r} candidates={labels} "
                    f"-> chosen={chosen!r} scores={scored}"
                )
                collisions_reported += 1

        buf.append(chosen.lower())
        in_file += 1

        if in_file >= args.tokens_per_lab:
            flush()

    flush()

    print(
        f"Done. tokens_processed={processed} files_written={files_written} "
        f"tokens_per_lab={args.tokens_per_lab} oov_skipped={oov_skipped} "
        f"collisions={collisions} out={args.out}"
    )


if __name__ == "__main__":
    main()

# python ./semestral/get_train_labs_from_corpus.py --dict semestral/dict_test.cz   --corpus semestral/train_text_korpus_big.txt   --out semestral/labs   --dict-encoding utf-8   --corpus-encoding cp1250   --out-encoding utf-8   --tokens-per-lab 100   --report-collisions 0
#
# nelze pouze od diakritikovat slova pro vytvoreni labelu, nutno dle jiz existujiciho pseudo slovniku, pro zachovani spravneho labelu -> pseudo phone tvar
# v pripade kolize vyslovnosti s gramatikou
# (nekolik gramatickych tvaru na jeden pseudo phone tvar -> levensteinova vzdalenost originalniho slova bez diakritiky s labelem)
# slo by i jenom oddiakritikovat a kontrolovat jestli existuje k label i label1 a pak az volat pseudo phone porovnani a bylo by to i rychlejsi