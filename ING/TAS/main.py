#!/usr/bin/env python3
"""
NP problém: 0/1 Batoh (Knapsack)
- brute force (ověření všech podmnožin)
- heuristika: greedy (poměr hodnota/váha) + jednoduché lokální prohledávání (hill-climb)

Použití:
  python main.py solve --n 24 --seed 123 --method brute
  python main.py solve --n 200 --seed 123 --method heur
  python main.py benchmark --n-min 10 --n-max 35 --step 1 --trials 3 --out results.csv

Poznámka:
- Brute force roste ~2^n. Nad určitý n se čas prudce zhorší.
- Heuristika je rychlá, ale nemusí být optimální.
"""
from __future__ import annotations
import argparse, csv, math, random, time, statistics
from typing import List, Tuple

def random_instance(n: int, seed: int = 0) -> Tuple[List[int], List[int], int]:
    rnd = random.Random(seed)
    weights = [rnd.randint(1, 50) for _ in range(n)]
    values  = [rnd.randint(1, 100) for _ in range(n)]
    capacity = int(sum(weights) * rnd.uniform(0.35, 0.45))
    return weights, values, capacity

def knapsack_bruteforce(weights: List[int], values: List[int], capacity: int) -> Tuple[int, int]:
    """Vrátí (best_value, best_mask). Hrubá síla: všechny podmnožiny."""
    n = len(weights)
    best_v = 0
    best_m = 0
    for m in range(1 << n):
        w = 0
        v = 0
        for i in range(n):
            if (m >> i) & 1:
                w += weights[i]
                if w > capacity:
                    v = -1
                    break
                v += values[i]
        if v > best_v:
            best_v, best_m = v, m
    return best_v, best_m

def knapsack_greedy_ratio(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """Greedy podle poměru hodnota/váha."""
    items = list(range(len(weights)))
    items.sort(key=lambda i: values[i] / weights[i], reverse=True)
    w = v = 0
    chosen = []
    for i in items:
        if w + weights[i] <= capacity:
            w += weights[i]
            v += values[i]
            chosen.append(i)
    return v, chosen

def knapsack_local_search(weights: List[int], values: List[int], capacity: int,
                         start: List[int], iters: int = 5000, seed: int = 0) -> Tuple[int, List[int]]:
    """
    Jednoduché lokální prohledávání:
    - start = greedy řešení
    - opakovaně zkusíme náhodně přepnout 1 položku (1-bit flip)
    - přijmeme jen pokud je řešení přípustné a nezhorší hodnotu
    """
    rnd = random.Random(seed)
    n = len(weights)
    state = [0]*n
    for i in start:
        state[i] = 1

    def eval_state(s):
        w = 0
        v = 0
        for i in range(n):
            if s[i]:
                w += weights[i]
                v += values[i]
        return w, v

    w_cur, v_cur = eval_state(state)
    best = state[:]
    v_best = v_cur

    for _ in range(iters):
        j = rnd.randrange(n)
        state[j] ^= 1
        w_new, v_new = eval_state(state)
        if w_new <= capacity and v_new >= v_cur:
            w_cur, v_cur = w_new, v_new
            if v_cur > v_best:
                best = state[:]
                v_best = v_cur
        else:
            state[j] ^= 1

    chosen = [i for i in range(n) if best[i]]
    return v_best, chosen

def solve_instance(n: int, seed: int, method: str, ls_iters: int) -> None:
    weights, values, cap = random_instance(n, seed=seed)
    print(f"n={n}, capacity={cap}")
    if method == "brute":
        t0 = time.perf_counter()
        opt_v, mask = knapsack_bruteforce(weights, values, cap)
        t1 = time.perf_counter()
        chosen = [i for i in range(n) if (mask >> i) & 1]
        print(f"BRUTE: value={opt_v}, items={len(chosen)}, time={t1-t0:.6f}s")
        print("chosen indices:", chosen)
    else:
        t0 = time.perf_counter()
        g_v, g_chosen = knapsack_greedy_ratio(weights, values, cap)
        ls_v, chosen = knapsack_local_search(weights, values, cap, g_chosen, iters=ls_iters, seed=seed)
        t1 = time.perf_counter()
        print(f"HEUR:  greedy={g_v}, final={ls_v}, items={len(chosen)}, time={t1-t0:.6f}s")
        print("chosen indices:", chosen)

def benchmark(n_min: int, n_max: int, step: int, trials: int, seed0: int,
              ls_iters: int, out_csv: str, brute_timeout_s: float | None) -> None:
    """
    Pro každý n v rozsahu:
      - vygeneruje 'trials' instancí
      - změří čas a kvalitu heuristiky (pokud brute doběhne)
    """
    ns = list(range(n_min, n_max + 1, step))
    rows = []
    for n in ns:
        brute_times, brute_vals = [], []
        heur_times, heur_vals = [], []
        brute_ok = True
        for t in range(trials):
            weights, values, cap = random_instance(n, seed=seed0 + n*1000 + t)

            # brute (s volitelným timeoutem)
            opt_v = None
            bt = None
            if brute_ok:
                t0 = time.perf_counter()
                # jednoduchý timeout kontrolujeme periodicky po blocích masek
                best_v = 0
                best_m = 0
                start = t0
                for m in range(1 << n):
                    w = 0
                    v = 0
                    for i in range(n):
                        if (m >> i) & 1:
                            w += weights[i]
                            if w > cap:
                                v = -1
                                break
                            v += values[i]
                    if v > best_v:
                        best_v, best_m = v, m
                    if brute_timeout_s is not None and (m & 0x3FFFF) == 0:  # kontrola každých ~262k masek
                        if time.perf_counter() - start > brute_timeout_s:
                            brute_ok = False
                            break
                if brute_ok:
                    bt = time.perf_counter() - t0
                    opt_v = best_v

            # heuristika
            t2 = time.perf_counter()
            g_v, g_chosen = knapsack_greedy_ratio(weights, values, cap)
            hs_v, _ = knapsack_local_search(weights, values, cap, g_chosen, iters=ls_iters, seed=seed0 + t)
            ht = time.perf_counter() - t2

            heur_times.append(ht); heur_vals.append(hs_v)
            if brute_ok:
                brute_times.append(bt); brute_vals.append(opt_v)

        row = {
            "n": n,
            "heur_time_s": statistics.mean(heur_times),
            "heur_value": int(statistics.mean(heur_vals)),
        }
        if brute_ok and brute_times:
            row["brute_time_s"] = statistics.mean(brute_times)
            row["brute_value"]  = int(statistics.mean(brute_vals))
            row["heuristic/optimal"] = row["heur_value"] / row["brute_value"] if row["brute_value"] else 1.0
        else:
            row["brute_time_s"] = ""
            row["brute_value"] = ""
            row["heuristic/optimal"] = ""
        rows.append(row)
        print(row)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["n","brute_time_s","brute_value","heur_time_s","heur_value","heuristic/optimal"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nsaved to {out_csv}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("solve")
    sp.add_argument("--n", type=int, required=True)
    sp.add_argument("--seed", type=int, default=0)
    sp.add_argument("--method", choices=["brute","heur"], default="heur")
    sp.add_argument("--ls-iters", type=int, default=5000)

    bp = sub.add_parser("benchmark")
    bp.add_argument("--n-min", type=int, default=10)
    bp.add_argument("--n-max", type=int, default=40)
    bp.add_argument("--step", type=int, default=1)
    bp.add_argument("--trials", type=int, default=3)
    bp.add_argument("--seed0", type=int, default=123)
    bp.add_argument("--ls-iters", type=int, default=5000)
    bp.add_argument("--out", type=str, default="results.csv")
    bp.add_argument("--brute-timeout-s", type=float, default=30.0,
                    help="Timeout na brute force pro jedno n (sekundy). Nastavte None pro bez omezení.")

    args = ap.parse_args()
    if args.cmd == "solve":
        solve_instance(args.n, args.seed, args.method, args.ls_iters)
    else:
        timeout = args.brute_timeout_s
        if str(timeout).lower() == "none":
            timeout = None
        benchmark(args.n_min, args.n_max, args.step, args.trials, args.seed0, args.ls_iters, args.out, timeout)

if __name__ == "__main__":
    main()
