library(readxl)
library(MASS)

setwd("~/Programming/DataScience")

x <- read_excel("Amerika/cv7/P0521b.xlsx")
x <- as.numeric(unlist(x))

plot(hist(x))

# creare vector of 79 zeros and 1 last 1
cens <- c(rep(0, 79), 1)
freq <- c(rep(1, 79), 21)
val <- 0.05 # hladina vyznamnosti
# creare vector of zeros
fit_weibull <- fitdistr(x, "weibull", start=list(shape=1, scale=1), lower=c(0, 0), cens, freq)
shape <- fit$estimate[1]
scale <- fit$estimate[2]

# matlab:
# wblfit(x, 0.05, cens, freq)

# susi
# mozna zkusit survreg() function from the survival