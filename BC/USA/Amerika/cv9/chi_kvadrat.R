# 6.4 chi kvadrat rozdeleni
# pr. 22 - Zjistěte 5 a 95% kvantil chí kvadrát rozdělení s 10 stupni volnosti
# chi2inv() - protoze znam quantil a zajima me hodnota na svisle ose
# 2 cally - chi2inv(0.05, 10) a chi2inv(0.95, 10)

quantile5 <- qchisq(0.05, df = 10, lower.tail = TRUE)
quantile95 <- qchisq(0.95, df = 10, lower.tail = TRUE)

print(quantile5)
print(quantile95)