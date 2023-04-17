# pr 26. normalni distribuce cv7
#a)
# what is the probabilty that the value is between -2 and 5
mean <- 0
deltaSq <- 3

x <- seq(-10, 10, by = 0.01)

o <- pnorm(5, mean, deltaSq) - pnorm(-2, mean, deltaSq)
# normcdf(5, 0, 3) - normcdf(-2, 0, 3)
print(o)

#b)
# there are 3 values what is the probality that at least one of them is in the range between -2 and 5

probToFail <- (1 - o)
proToSuccess <- o
# matlab:
# bincdf(2, 3, 1 - o) or binpdf(3, 3, 1 - o)
o2 <- pbinom(2, 3, proToSuccess)
o3 <- 1 - dbinom(3, 3, proToSuccess)
print(o2)
print(o3)

# watch the normal distribution video