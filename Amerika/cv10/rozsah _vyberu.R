# pr. 13 z kapitoly 7.5 rozsah vyberu
# pri odhadu volebnich vysledku chceme, aby sirka intervalu volebniho vysledku majici odhadem 20 % hlasu
# byla maximalne 2 %. Urcete rozsah vyberu pro 95 % intervalovy odhad
# pocitani pomoci vzorce:
# n >= 4 * p * (1 - p) * (Z1 - alpha/2)^2 / (trojuhelnik_max)^2
# => 4 * 0.2 * 0.8 * (normiv(0.975, 0, 1))^2 / (0.02)^2
# norminv(0.975, 0, 1) = 1.959964
#
# n >= 4 * 0.2 * 0.8 * (1.959964)^2 / (0.02)^2 = 3841.472
# tohle vymyslel copilot

# kapitola 7.7 intervalovy odhad parametru spojitych rozdeleni
# pr. 16a
# doba do poruchy...
