# regularni vyrazy

regularni vyraz popisuje regularni jazyk, ten je rozpoznatelny konecnym automatem

## zasobnikovy automat

zasobnikovy automat je rozsireni konecneho automatu o zasobnik, ktery muze slouzit jako pamet
rozpoznani slova urcuje prazdnost zasobniku

Q = konecna mnozina stavu
Sigma = konecna mnozina vstupnich symbolu (abeceda)
Gamma = konecna mnozina symbolu zasobniku
delta = prechodova funkce (Q x (Sigma U {epsilon}) x (Gamma U {epsilon}) -> mnozina (Q x (Gamma U {epsilon})))
q0 = pocatecni stav
Z0 = pocatecni symbol zasobniku

delta: Q x (Sigma U {epsilon}) x (Gamma U {epsilon}) -> mnozina (Q x (Gamma U {epsilon}))

(x,y,z) -> (p,w) kde
x = aktualni stav
y = symbol na vstupu (nebo epsilon)
z = symbol na vrcholu zasobniku (nebo epsilon)
p = novy stav
w = symboly, ktere se vlozi na zasobnik (mohou byt i 2 a vice symbolu)
