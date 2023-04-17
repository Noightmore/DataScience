# normal distribution
# pr. 24 z normalni distribuce cv7
mean <- 5
deltaSq <- 4 # use root of deltaSq

x <- seq(-10, 10, by = 0.01)
#o  <- dnorm(x, mean, deltaSq, log = FALSE)
o <- qnorm(0.2, mean = 5, sd = 2) # norminv(0.2, 5, 2)
print(o)

o <- qnorm(0.5, mean = 5, sd = 2) # norminv(0.5, 5, 2)
print(o)

o <- pnorm(3.5, 5, 2) # normcdf(3.5, 5, 2)
print(o)