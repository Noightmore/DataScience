# pr. 28 fisher-schne
# matlab: finv(0.05, 10, 5)
# 28: Zjistěte 5 a 95 % kvantil F rozdělení s 10 a 5 stupni volnosti. Dále určete 5 a 95% kvantil F
# rozdělení s 5 a 10 stupni volnosti. Zkuste odhadnout jaký je mezi výsledky vztah.

quantile5 <- qf(0.05, df1 = 10, df2 = 5, lower.tail = TRUE)
quantile95 <- qf(0.95, df1 = 10, df2 = 5, lower.tail = TRUE)

print(quantile5)
print(quantile95)

quantile5 <- qf(0.05, df1 = 5, df2 = 10, lower.tail = TRUE)
quantile95 <- qf(0.95, df1 = 5, df2 = 10, lower.tail = TRUE)

print(quantile5)
print(quantile95)