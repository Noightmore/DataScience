# 8.3 Vícevýběrové testy
# 8.3.1
# Test shody rozptylů
# Př. 25: Výrobní stroj se seřídí začátkem směny. Kontrola výrobků probíhá vždy po jedné hodině a
# chceme zjistit, zda nedochází k většímu rozptylu určitého rozměru. Otestujte na hladině významnosti
# 5 %, zda rozptyly dat jsou shodné. Použijte Bartlettův i Leveneův test.
# x1=[18,19,19,19,20,21,21,22,22,23,23,24,24,24,25,25,25,26,26,26,27,28];
# x2=[17,18,18,19,19,20,21,21,22,22,22,23,23,23,23,24,24,25,25,26,26,27,28,29] ;
# x3=[16,17,18,18,18,19,20,20,20,20,21,21,21,22,23,23,23,24,25,26,27,27,28,28,29,31];
# x4=[14,15,16,16,17,18,19,20,22,22,22,23,24,25,25,27,27,27,28,28,28,31,31,33,34];
# [rozptyly nejsou shodné, a) pval=0.0041, b) pval=0.000216]
#install.packages("car")

library(stats)
library(car)

x1 <- c(18,19,19,19,20,21,21,22,22,23,23,24,24,24,25,25,25,26,26,26,27,28)
x2 <- c(17,18,18,19,19,20,21,21,22,22,22,23,23,23,23,24,24,25,25,26,26,27,28,29)
x3 <- c(16,17,18,18,18,19,20,20,20,20,21,21,21,22,23,23,23,24,25,26,27,27,28,28,29,31)
x4 <- c(14,15,16,16,17,18,19,20,22,22,22,23,24,25,25,27,27,27,28,28,28,31,31,33,34)

x2 <- x2[1:22]
x3 <- x3[1:22]
x4 <- x4[1:22]

#bartlett.test(x1, list(x1,x2,x3,x4))

# in matlab: vartestn(x1, skupina) - skupina -> [x1,x2,x3,x4]
data <- numeric(data.frame(x1,x2,x3,x4))

# tohle susi neskutecne