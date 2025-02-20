# 7.7 Intervalový odhad parametrů spojitých rozdělení
# Př. 16a: Doba do poruchy nedegradujícího výrobku je popsána exponenciálním rozdělením.
# Prováděla se zkouška 50 výrobků po dobu 1000 hodin. Po poruše nebyly výrobky nahrazovány. Bylo
# zjištěno 10 poruch, u ostatních 40 výrobků byla zkouška ukončena v čase 1000 hodin. Určete
# parametr exponenciálního rozdělení a jeho 95% intervalový odhad.

#Tporuch=[80,160,240,320,400,560,720,800,900,960]
#[stredni hodnota je 4514 h, intervalovy odhad <2642,9413> h]

t_poruch <- c(80, 160, 240, 320, 400, 560, 720, 800, 900, 960)

# mean(t_poruch)
m <- mean(t_poruch)

# in matlab:
# params: data, alpha, cens (jakym zpusobem mam ukoncenou udalost poruchou/casem 0/1)
# - cens musi mit stejne delku vektoru jako data, posledni je frekvence
# - frekvence - opet stene delka vektoru jako data, pro kazdy prvek vektoru data zapiseme pocet kolikrat
# se kazdy vyrobek v danem case porouchal - pro vsechny to je 1 a u 1000 - posledniho prvku to je 40
# [par, io] = expfit(t_poruch, 0.05, cens, freq)

# todo: learn R equivalent

