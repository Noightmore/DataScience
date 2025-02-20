# Př.6: Při kontrole životnosti 50 výrobků bylo z dat zjištěno, že střední doba do poruchy výrobku je
# 27400 hodin a směrodatná odchylka 5400 hodin (popsáno normálním rozdělením). Určete na hladině
# významnosti 5 %, zda lze přijmout fakt výrobce, že střední doba do poruchy je rovna 30 000 hodin.
# [H0 nepřijímáme,pvalue=0.0013]

# mean = 27400
# idk = 5400
# vyuzit kapitolu 8.3.2
#
# in matlab:
# H0 = ny = 30000, HA -> ny != 30000
# testovaci kriterium:
# T = (x_dash - ny)/s * sqrt(n) = (27400 - 30000)/5400 * sqrt(50) = -3.4 (jedna moznost vypoctu)
# - nutno si to poradne predstavit, malo vzorku = studentovo rozdeleni
#  overeni hypotesy in matlab: tinv(0.025, 49) = - 1.97, druhy bod: tinv(0.975, 49) =  1.97 (druha moznost vypoctu)
# vysvetleni: kapitola 8.3.2 test stredni hodnoty normalniho rozdeleni - seznam hypotez (popsane)
# vysledek: H0 zamitam

# pres p-value: p = 2 * tcdf(-3.4, 49) = 0,0012 (plocha)

# Find the t-value
# nene tohle je sus:
t_value <- pt(qt(0.975, 49), 49, lower.tail = FALSE) + pt(qt(0.05, 49), 49, lower.tail = FALSE)
# Print the t-value
cat("t-value =", t_value, "\n")

# this is correct:
T <- (27400 - 30000)/5400 * sqrt(50)
cat(T)

# 8.1.3 - parovy test
# Př. 7: Mějme následující data, kde první řádek představuje hodnotu parametru před tepelnou
# úpravou (vzorek 1, řádek 1) a v druhém řádku jsou uvedeny výsledky na stejných kusech po tepelné
# úpravě (vzorek 2, řádek 2). Data jsou z normálního rozdělení. Zjistěte na hladině významnosti 5 %,
# zda:

  # x=[35.0,36.0,36.3,36.8,37.2,37.6,38.3,39.1,39.3,39.6,39.8,37.2,38.1,38.2,37.9,37.6,38.3,39.2,39.4,39.7,39.9,39.9];

#A) Je shodná hodnota parametru u obou výběrů H0: ny1 = ny2, H1: ny1 != ny2
# 2. argument 0 = rozdil
# in matlab: [h, p, ci, stat] = ttest(x, 0, 0.05, 'both')
# kdyby doslo ke snizeni o 10 po operaci -> H0: ny_pred = ny_po+10 H1(alternativni): ny1 != ny2
x <- c(35.0, 36.0, 36.3, 36.8, 37.2, 37.6, 38.3, 39.1, 39.3, 39.6, 39.8, 37.2, 38.1, 38.2, 37.9, 37.6, 38.3, 39.2, 39.4, 39.7, 39.9, 39.9)

# toto taky susuje:
H  <- t.test(x, mu = 0, alternative = "two.sided", conf.level = 0.95)

print(H)

# odpoved: zamitame H0
# B) došlo ke zvýšení parametru po tepelné úpravě. H0: ny1 >= ny2, H1: ny1 < ny2

# 8.1.4: znamenkovy test
# Př. 8: Mějme data: x=[-6,-3,-1,0,2,3,5,6,7,8,9,11,12,14,15,18,22,28,32,37,41]. Otestujte na hladině
# významnosti 5 % znaménkovým testem, zda medián je roven 25.
# Pozn: Nepředpokládáme, že data jsou z normálního rozdělení
# [Na hladině významnosti 5 % zamítáme H0, že median je roven 25, pval=0.0072].

# H0: x_0.5 = 25, H1: x_0.5 !- 25
# in matlab: [p,h] = signtest(x, 25)
# p = 0.0072
# odpoved: na hladine vyznamnosti 5 % zamitame hypotezu H1

# 8.2 Dvouvýběrový test
# 8.2.1
# Dvouvýběrový test – test shody dvou rozptylů
# Př. 16: Balicí zařízení je seřízeno na začátku ranní směny a následně kontrolováno u odpolední směny.
# Byly zjištěny následující hodnoty hmotnosti výrobků:

# Ráno=[98.5, 98.6, 98.7, 98.7, 98.7, 98.8, 98.9, 99.2, 99.3, 99.3] g
# Odpoledne=[98.1,98.2, 98.3, 98.4, 98.6, 98.7, 98.8, 98.9, 99.0, 99.0] g
# Otestujte na hladině významnosti 5 %, zda je shodné seřízení stroje, tj. zda rozptyl hmotnosti výrobku
# je shodný.
# [Nezamítáme hypotézu H0 na hladině významnosti 5 % o shodě rozptylů, pvalue=0.7187]

# H0: rozptyl rano = rozptyl odpoledne
#[h, p, ci, stat] = vartest2(rano, odpoledne, 0.05, 'both')
# vysledek H = 0, na hladine vyznamnosti 5 % prijimame hypotezu o shode roptylu

rano <- c(98.5, 98.6, 98.7, 98.7, 98.7, 98.8, 98.9, 99.2, 99.3, 99.3)
odpoledne <- c(98.1,98.2, 98.3, 98.4, 98.6, 98.7, 98.8, 98.9, 99.0, 99.0)

# divne susi, pouzit matlab
h <- var.test(rano, odpoledne, 0.95, alternative = "two.sided" )
print(h)