# random priklady ze cviceni
- hygepdf - zavisly pokusy
- binpdf - nezavisle pokusy

mame balicek mariasovych karet 10 krat losujeme kartu, kterou nasledne nevracime do balicku
urcete pravdepodobnost, ze:

a) vylosujeme 8 karet a to bud spodky, filky, krale a esa
-> hygepdf(8, 32, 16, 10) ((16 over 8) * (16 over 2))/(32 over 10)

b) vylosujeme prave 2 esa, 3 krale, 2 filky, 1 spodka
p = (4 over 2) * (4 over 3) * (4 * 2) * (4 over 1) * (16 over 2) / (32 over 10)

a) vracime karty zpatky:
p = binopdf(8, 10, 16/32) (10 over 8) * 0.5^8 * (1* 0.5)^2

b) vracime karty

mnpdf([2,3,2,1,2], [4/32, 4/32, 4/32, 4/32, 16/32])
= (10! / (2! * 3! * 2! * 1! * 2!) ) * (1/8)^2 * (1/8)^3 * (1/8)^2 * (1/8)^1 * (1/8)^2

poisson rozdeleni - poisopdf
poispdf (matlab) = dpois in R
poiscdf (matlab) = ppois in R

jednotky na hodinu, kilometry, sekundy, kusy
chyba na stranku atd.

lze z hypergeometrickeho rozdeleni prejit na binomicke

TODO: dostudovat si parametry jednotlivych distribucnich funkci
+ aproximace z binom na poisonovo