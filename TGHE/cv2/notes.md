# GRAFY

- minimalni kostra grafu
- minimalni cesta
- toky v siti

izomorfismus -> grafy jsou zamenitelne, stejne jen jinak zakreslitelne, jinak pojmenovane vrcholy
overeni zda jsou 2 grafy izomorfni -> slozitost NP, nelze vyjadrit polynomem, avsak vysledek algoritmu lze overit

uplny graf -> nelze uz pridat dalsi hranu aniz by vznikla nasobna hrana, kazdy 
- n over 2 -> pocet hran uplnyho grafu, n = pocet vrcholu n(n-1)/2

## operace s grafy
- pridani/odebrani vrcholu (u odebirani vrcholu musim odebrat i vsechny hrany, ktere do daneho vrcholu jdou)
- pridani/odebrani hrany (kontrola, zda vrcholy existuji)

tah/sled/minimalni cesta
tah - nesmim do stejneho bodu 2 krat
kruznice - zacina ve stejnym bode, kde i konci
hammiltonovska kruznice - kruznice, ktera je na vsech  vrcholech
bipartilni graf - 2 barvy kazda hrana spojuje 2 vrcholy, kazdy jine barvy
rovinny graf -> jsem schopen nakreslit hrany tak, aby se vzajemne nekrizily
souvisly graf -> existuje cesta mezi libovolnymi 2 vrcholy
orientovany graf -> pridaji se smery hran

todo: videos about comptetitive programming?