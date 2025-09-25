Konecny automat

formalni definice: A = (Q, Sigma, delta, q0, F)
Q = neprazdna konecna mnozina stavu
Sigma = neprazdna konecna mnozina symbolu (abeceda)
delta: Q x Sigma -> Q prechodova funkce
q0 elem Q pocatecni stav
F subseteq Q mnozina koncovych stavu

priklady typu automatu jsou na fotce z 23.9.2025

Nedeterministicky konecny automat

N = (Q, Sigma, delta, I, F)

I = pocatecni stavy (mnozina)

Omezeni konecneho automatu

pamatuje si pouze skrz stavy
neumi pocitat do nekonecna
nerozpoznava jazyk {a^n b^n | n >= 0}, musim z hora omezit n, pak to lze