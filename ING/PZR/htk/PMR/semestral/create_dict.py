#!/usr/bin/env python3
import argparse
import unicodedata
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, Counter as CounterType, List, Tuple, Optional
import concurrent.futures
import os
import sys

from antlr_fun.fun import rewrite_text

# Optional tqdm progress bar
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

WORD_RE = re.compile(r"\w+", flags=re.UNICODE)


def strip_diacritics(s: str) -> str:
    """Remove diacritics from a Unicode string (for Czech keys)."""
    nfkd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch))


def tokenize(text: str) -> List[str]:
    """Basic word tokenizer preserving letters (incl. Czech)."""
    return WORD_RE.findall(text)


def process_chunk(text: str) -> Dict[str, CounterType[str]]:
    """
    Process a text chunk and return:
        { base_key (no diacritics, upper) : Counter({pron: count, ...}) }
    """
    base_to_pron_counts: Dict[str, CounterType[str]] = defaultdict(Counter)

    for token in tokenize(text):
        if not token:
            continue
        lowered = token.lower()
        base_key = strip_diacritics(lowered).upper()
        phones = rewrite_text(token)
        base_to_pron_counts[base_key][phones] += 1

    return base_to_pron_counts


def merge_results(
        accum: Dict[str, CounterType[str]],
        part: Dict[str, CounterType[str]],
) -> None:
    """Merge partial {base_key: Counter(pron)} into accum in-place."""
    for base, ctr in part.items():
        accum[base].update(ctr)


def make_line_chunks(
        lines: List[str],
        workers: int,
) -> Tuple[List[Tuple[str, int, int]], List[int]]:
    """
    Split lines into many small chunks and assign them to worker slots.

    Returns:
      chunks: list of (chunk_text, chunk_size_in_lines, slot_id)
      slot_totals: list of total lines assigned to each slot
    """
    total = len(lines)
    if total == 0:
        return [], [0] * workers

    # Aim for about 10 * workers chunks, at least 1000 lines per chunk
    target_chunks = max(10 * workers, 1)
    approx_lines_per_chunk = max(1000, total // target_chunks)

    chunks: List[Tuple[str, int, int]] = []
    slot_totals = [0] * workers
    slot = 0

    for i in range(0, total, approx_lines_per_chunk):
        chunk_lines = lines[i : i + approx_lines_per_chunk]
        size = len(chunk_lines)
        if size == 0:
            continue
        chunk_text = "".join(chunk_lines)
        chunks.append((chunk_text, size, slot))
        slot_totals[slot] += size

        # round-robin slot assignment
        slot = (slot + 1) % workers

    return chunks, slot_totals


def assign_dict_keys(
        base_to_pron_counts: Dict[str, CounterType[str]]
) -> List[Tuple[str, str, int]]:
    """
    Convert {base_key: Counter({pron: count})} -> list of
    (dict_key, pron, freq).
    """
    entries: List[Tuple[str, str, int]] = []

    for base_key, pron_counter in base_to_pron_counts.items():
        # Sort pronunciations by frequency (desc) then lexicographically
        sorted_prons = sorted(
            pron_counter.items(),
            key=lambda x: (-x[1], x[0]),
        )

        if len(sorted_prons) == 1:
            pron, freq = sorted_prons[0]
            dict_key = base_key
            entries.append((dict_key, pron, freq))
        else:
            for idx, (pron, freq) in enumerate(sorted_prons):
                if idx == 0:
                    dict_key = base_key
                else:
                    dict_key = f"{base_key}{idx}"
                entries.append((dict_key, pron, freq))

    return entries


def build_dictionary(
        input_path: Path,
        workers: int = 1,
        encoding: str = "utf-8",
) -> List[Tuple[str, str, int]]:
    """
    Build the HTK-style dictionary entries from input text.
    Returns list of (word_key, phones, frequency).
    """
    text_lines = input_path.read_text(
        encoding=encoding,
        errors="ignore"
    ).splitlines(keepends=True)

    total_lines = len(text_lines)

    if workers is None or workers < 1:
        workers = 1

    base_to_pron_counts: Dict[str, CounterType[str]] = defaultdict(Counter)

    # ----- Single-process path with fine-grained progress -----
    if workers == 1:
        if tqdm is not None:
            pbar = tqdm(total=total_lines, desc="Worker0", unit="lines")
        else:
            pbar = None

        for idx, line in enumerate(text_lines, start=1):
            for token in tokenize(line):
                if not token:
                    continue
                lowered = token.lower()
                base_key = strip_diacritics(lowered).upper()
                phones = rewrite_text(token)
                base_to_pron_counts[base_key][phones] += 1

            if pbar is not None:
                pbar.update(1)
            elif idx % 100000 == 0:
                print(
                    f"Processed {idx}/{total_lines} lines",
                    file=sys.stderr,
                    flush=True,
                )

        if pbar is not None:
            pbar.close()

    # ----- Multiprocessing path with per-worker bars -----
    else:
        chunks, slot_totals = make_line_chunks(text_lines, workers)

        if tqdm is not None:
            # One global bar + one per worker slot
            total_bar = tqdm(
                total=total_lines,
                desc="Total",
                unit="lines",
                position=0,
                leave=True,
            )
            worker_bars = [
                tqdm(
                    total=slot_totals[i],
                    desc=f"W{i}",
                    unit="lines",
                    position=i + 1,
                    leave=True,
                )
                for i in range(workers)
                if slot_totals[i] > 0
            ]
            # Map slot id -> bar index in worker_bars
            slot_to_bar_idx = {}
            idx_counter = 0
            for i in range(workers):
                if slot_totals[i] > 0:
                    slot_to_bar_idx[i] = idx_counter
                    idx_counter += 1
        else:
            total_bar = None
            worker_bars = []
            slot_to_bar_idx = {}

        with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as ex:
            future_to_meta = {}
            for chunk_text, size, slot in chunks:
                fut = ex.submit(process_chunk, chunk_text)
                future_to_meta[fut] = (size, slot)

            for fut in concurrent.futures.as_completed(future_to_meta):
                part = fut.result()
                merge_results(base_to_pron_counts, part)

                size, slot = future_to_meta[fut]

                if total_bar is not None:
                    total_bar.update(size)

                if slot in slot_to_bar_idx:
                    worker_bar = worker_bars[slot_to_bar_idx[slot]]
                    worker_bar.update(size)
                else:
                    if total_bar is None:
                        # crude fallback
                        print(
                            f"Completed chunk of ~{size} lines (slot {slot})",
                            file=sys.stderr,
                            flush=True,
                        )

        if total_bar is not None:
            total_bar.close()
            for bar in worker_bars:
                bar.close()

    entries = assign_dict_keys(base_to_pron_counts)
    entries.sort(key=lambda x: (-x[2], x[0]))
    return entries


def write_dictionary(
        entries: List[Tuple[str, str, int]],
        output: Optional[Path] = None,
) -> None:
    """
    Write HTK-style dictionary: WORD<TAB>PHONES<TAB>FREQ
    """
    lines = []
    for word, phones, freq in entries:
        lines.append(f"{word}\t{phones}\t{freq}")

    text = "\n".join(lines) + "\n"

    if output is None:
        print(text, end="")
    else:
        # cp1250 for HTK-style Czech dicts
        output.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build HTK-style dictionary with frequencies from a large Czech text corpus. "
                    "NOT ASCII ORDERED but frequency ordered"
    )
    p.add_argument("--input", "-i", type=Path, required=True,
                   help="Input text file")
    p.add_argument(
        "-o", "--output", type=Path, default="./dict",
        help="Output dictionary file (default: ./dict)"
    )
    p.add_argument(
        "-w", "--workers", type=int, default=os.cpu_count(),
        help="Number of worker processes (default: number of CPU cores)"
    )
    p.add_argument(
        "-e", "--encoding", type=str, default="cp1250",
        help="Input file encoding (default: cp1250)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    entries = build_dictionary(
        args.input,
        workers=args.workers,
        encoding=args.encoding,
    )
    write_dictionary(entries, args.output)


if __name__ == "__main__":
    main()
