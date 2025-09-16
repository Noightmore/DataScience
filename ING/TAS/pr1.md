# prednaska 1 

budou 2 semestralni prace na zapocet

## teorie mnozin

co to je, jak se zapisuji, zakladni vlastnosti, zname

mnozina obsahujici prazdnou mnozinu neni prazdna mnozina.

{prazdna mnozina} != prazdna mnozina

### potencni mnozina

znacime: P(X)
mnozina vsech podmnozin mnoziny X
P(x) = {prazdna mnozina, {a}, {b}, {a,b}} pro X = {a,b}
|P(X)| = 2^|X| (velikost potencni mnoziny je 2 na velikost mnoziny)

### zakladni operace s mnozinami
prunik, sjednoceni, doplnek, rozdil, podmozina

rozdil neni komutativni operace, co lezi v jedne a nelezi v druhe

### pojem kartenzsky soucin
usporadene dvojice (x,y) takova ze zavisi na poradi, pokud x != y

definice:
X x Y = {(x,y) | x elem X, y elem Y}

X = {1,2}
X^2 = X x X = {(1,1), (1,2), (2,1), (2,2)}

### Relace
relace je podmnozina kartenzskeho soucinu R

vlastnosti relaci:
- reflexivni: pro kazde x elem X plati (x,x) elem R
- symetricka: pro kazde x,y elem X plati (x,y) elem R => (y,x) elem R
- transitivni: pro kazde x,y,z elem X plati (x,y) elem R a (y,z) elem R => (x,z) elem R

mame matici kazdy s kazdym
reflexivita je kazdy prvek s nim samym
symetrie x -> y a y -> x, oba smery
transitivita x -> y a y -> z => x -> z (ja se kamaradim s radkem, 
on se kamaradi s petrem, ale ja petra nesnasim -> poruseni transitivity)

doporuceni na literaturu: harry potter a
metody racionality

### Relace ekvivalence

relace na X^2, ktera je reflexivni, symetricka a transitivni

### Formalni jazyk

abeceda -- neprazdna konecna mnozina symbolu

A = {a,b, ...,z}
B = {0,1 ..., 9}

uzaver mnoziny A*; A+

epsilon je prazdny retezec

popisy jazyku, vyctem, vlastnosti, pravidla, gramatika, automat

abs(W) -- delka slova
spodni index -- pocet symbolu
pocet znaku ve slove delitelny tremi
n- nasobny vyskyt znaku -- a^n 
prazdny jazyk
jazyk obsahujici prazdne slovo  -- eps

### formalni jazyky v praxi

programovaci jazyky, prirozene jazyky, markup jazyky (html, xml), SQL

