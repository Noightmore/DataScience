# 6 face cube with 1, 2, 3, 4, 5, 6
mean <- sum(1:6) / 6
sd <- sqrt(sum((1:6 - mean)^2) / 6)

print(mean)
print(sd)

#dist <- pnorm(270, mean * 60 , sqrt(sd*60)) - pnorm(220, mean*60, sqrt(sd*60))
# normcdf - normal cumulative distribution function
# in R it is pnorm()
dist <- pnorm(270, mean * 60 , sqrt(sd*60)) - pnorm(220, mean*60, sqrt(sd*60))
print(dist)