library(R.matlab)
library(MASS)

# print current working dir
#getwd()
setwd("~/Programming/DataScience")
file <- readMat("Amerika/cv7/P0521a.mat")

x <- as.vector(file)
# get rid off nonnumeric values
x <- x[!is.na(x)]

# convert each item of vector x to be numeric
x <- as.numeric(unlist(x))

plot(x)
# mean(x) mozna prumer?
# startovaci vektor - todo: zjistit jak se to dela
fit <- fitdistr(x, "weibull", list(300, 5))
print(fit)
#shape <- fit$estimate[1]
#scale <- fit$estimate[2]

# matlab equivalent:
# x=importdata('P0521a.mat');
# wblfit(x)
# E(x),D(x) = wblstat(x)