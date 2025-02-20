# note: procvicit si tu geom pravdepodobnost

# distribucni funkce
# y = 1 - e^(-t/3)

t <- 0:100
y <- 1 - exp(-t/3)
plot(t, y, type = "l", xlab = "t", ylab = "y")

# pravdepodobnost ze bude v nejakym rozsahu je rozdil pravdepodobnosti
# jednoho koncoveho bodu s pravdepodobnosti druheho koncoveho bodu

# stejne prikazy jako v matlabu
#mean(y[1:3]) - mean(y[1:2])
#nanmean(y[1:10] - y[2:11])

# modus, shorth
#mode(y) - nejcastejsi hodnota
#shorth(y) - nejmensi interval, ve kterem lezi alespon 50 % hodnot

#median(y) - median
#nanmedian(y) - median, ignoruje NaN
#quantile(y, 0.5)
#prctile(y, 50)
#iqr(y) - interqvantylove rozpeti

#moment(y, 1) - urceni libovolneho centralniho rozptylu
#var(y) - rozptyl

#mad(y) - stredni hodnota absolutnich odchylek od stredni hodnoty

#skewness(y) - vyberova sikmost