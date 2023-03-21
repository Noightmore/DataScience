# load P0305.mat file

library(R.matlab)

file <- readMat("absolute-path-to-file") # .mat file
#print(file)

#plot(file$P0305[,1], file$P0305[,2], type="l", xlab="Time", ylab="Price", main="P0305")
#print(file[1])
#plot(file[1], type="l", xlab="Time", ylab="Price", main="P0305")

# convert x to vector
x <- as.vector(file)
# get rid off nonnumeric values
x <- x[!is.na(x)]

# convert each item of vector x to be numeric
x <- as.numeric(unlist(x))

#print(x)

# transform vector x  to vector y using this function below
y <- (1 - exp(-x/(3)))
#print(y)

#plot(x, y, type="l", xlab="x", ylab="y", main="P0305")
#hist(y, breaks=100, xlab="y", main="P0305")


# cviceni 3.5 ecdf funkce je distribucni fce nahodne veliciny:
# ecdf(x .* y)
# ecdf(x + y)

# funkce ecdf zaroven i plotne graf

#e <- ecdf(y * x)
#e <- ecdf(y + x)
e <- ecdf(log10(y/x))

# get the log base of 10 of each value of e
plot(e, xlab="y", ylab="F(y)", main="P0305")

