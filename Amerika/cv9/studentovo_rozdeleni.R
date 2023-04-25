# 6.5 studentovo rozdeleni
# pr. 25
# stupne volnosti s 2, 4, 10 a 100
# nabyva pravdepodobnost P(X > 1) urcete pravdepodobnost i pro normovane rozdeleni
a <- 1 - pt(1, c(2, 4, 10, 100)) # studentovo rozdeleni
print(a)
# in matlab = 1 - tcdf(1, [2, 4, 10, 100])

b <- qt(0.95, 10) # normovane rozdeleni
print(b)
# in matlab tinv(0.95, 10) = 1.8331