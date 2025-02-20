# "comment"
#"comment"

# vector of number from 1 to 100 with step 0.1
x <- seq(-20, 20, 0.1)
y <- x^2 + 11
#plot(x, y, type = "l", xlab = "x", ylab = "y", )
# add another point to the graph
#points(0, 11, pch = 16, col = "red")
#med <- median(y)

hist(y, breaks = 100, col = "red", main = "Histogram", xlab = "x", ylab = "y")

