# NP úloha – Batoh (0/1 knapsack)

Obsah:
- `main.py` – řešení (brute force + heuristika) + benchmark.
- `results_sample.csv` – ukázkový výstup (z tohoto prostředí).
- `runtime_plot.png`, `quality_plot.png` – ukázkové grafy.
- `zprava.docx` – šablona zprávy s vloženými ukázkovými grafy.

## Rychlé spuštění
```bash
python main.py solve --n 24 --seed 123 --method brute
python main.py solve --n 200 --seed 123 --method heur

# testování výkonu (brute s timeoutem 30 s pro jedno n)
python main.py benchmark --n-min 10 --n-max 40 --step 1 --trials 3 --out results.csv
```

## Jak určit limit < 1 hodina (brute force)
1. Udělejte benchmark pro rostoucí n (např. 20–35) s `--brute-timeout-s None` pro menší n.
2. Pro každé n máte čas t(n). Pro brute platí přibližně: t(n) ≈ c · 2^n.
3. Odhadněte c třeba jako medián t(n)/2^n (pro větší n).
4. Spočtěte n*, kde c · 2^n* = 3600 s → n* = log2(3600/c).
5. Potom ověřte spuštěním pro n okolo n* (např. n*−1, n*, n*+1).

Pozn.: Konkrétní n* závisí na vašem CPU.
