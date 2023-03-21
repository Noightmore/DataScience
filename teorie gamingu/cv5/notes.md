# cviceni 5

opakovani ze cviceni 4

## typy hran

stromova hrana AB -> time_in1A < time_in2B < time_out2B < time_out1A

zpetna hrana CA -> time_in2A < time_in1C < time_out1C < time_out2A

pricna hrana DC -> time_in2D < time_out2C < time_in1D < time_out1D

dopredna hrana AD time_in1A < time_in2D < time_out2D < time_out1A

1 - hrana vychazi z vrchulu
2 - hrana vchazi do vrcholu

aby byla v grafu kruznice musi zde byt dopredna, pricna, a zpetna hrana

treba se podivat na video, ktere se touto problematikou zabyva -> je v grafu kruznice?

halitosis hledani kruznice O(n + m) - pocet hran plus pocet vrcholu

prochazeni a mereni casu u orientovaneho grafu podle zvoleneho pocatecniho vrcholu 
nemusi vzdy vratit stejny pocet stromu pri kresleni stromu pruchodu do hloubky s casy

## topologicke usporadani

- neexistuji zde kruznice
- projdi graf do hloubky
- sserad vrcholy dle out od max po min? - random informace?


## silne souvisle komponenty

- vytvorim graf G, kde vsechny hrany jsou opacne orientovane od G
- G projdu do hloubky a a zaznamenam casy in a casy out
- projdu G do hloubky, vrcholy volim postupne podle casu out z pruchodu G od max po min
- kazdy vznikly strom je SSK - silne souvisla komponenta
- sloucim vrcholy SSK do metagrafu (metagraf je spojeni dvou silne souvislych komponent)

bruh