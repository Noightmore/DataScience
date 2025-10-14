# turinguv stroj

ts = (Q, SIGMA, P, GAMMA, q0, F)

q = stavy neprazdna mnozina 
SIGMA = vstupni abeceda
P = paskova abeceda SIGMA < P
q0 = pocatecni stav q0 ∈ Q
F = koncove stavy F ⊆ Q
GAMMA = mnozina symbolu na pase (prazdny symbol je v GAMMA, ale ne v SIGMA) (Q - F) x P -> Q x P x {-, 0, +} "kam posunout tu hlavu, pravo, levo, zustat"

tvar instrukci (q1, a) -> (q2, b, +)
- q1: soucasny stav
- a: precteny symbol na pase
- q2: novy stav
- b: symbol, ktery se zapise na pas
- +: posun hlavy doprava

## varianty TS
- TS s vice koncovymi stavy (q^+, q^-)
- TS s vnitrni pameti (zasobnik, fronta)
- TS s vice paskami, 3 -> vstupni, pracovni a vystupni
- nedeterministicky TS (vice moznosti instrukci pro dany stav a symbol)
### univerzalni TS 
- TS simulujici cinnost lib TS nad stejnou, nebo vetsi abecedou
- Q, gama, q0, F. Dokazeme zapsat
- dokazeme zakodovat v abecede SIGMA