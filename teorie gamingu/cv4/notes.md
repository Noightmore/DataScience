## matice incidence

- pocet radku = pocet vrcholu
- pocet sloupcu = pocet hran
- kazda bunka obsahuje 1 nebo 0 podle toho jestli dany vrchol je soucasti dane hrany

## laplasova  matice
- existence spojeni hrany s vrcholem

## pruchod do hloubky
graf
vlezem do vrcholu a pocitame cas nez projdem vsechny nasledovniky
in, out 

### pseudokod pruchodu do hloubky

    projdi(v)
        color(v) = gray
        time = time + 1
        in(v) = time
        for each w in sousedi(v) do
            if color(w) == white then
                projdi(w)
        color(v) = black
        time = time + 1
        out(v) = time

- pokud graf nespojity tak existuje vice stromu algoritmu
- cas se stale inkrementuje dal