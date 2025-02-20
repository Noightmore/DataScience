#we have got a special 20 face dice and each face is numbered in the following pattern: 10 faces contain number 1, 5 faces contain the number 2, 2 faces contain the number 3,
#1 face contains number 4,
#1 face contains number 10 and
#1 face contains number 0.
#We roll this dice 100 times. How would I compute the probability that the sum of the numbers we rolled is between 220 to 270 included?

# 1. create a vector of the number of faces for each number
# 2. create a vector of the number of times each number appears on the dice
face_values <- c(1, 2, 3, 4, 10, 0)
face_counts <- c(10, 5, 2, 1, 1, 1)

# compute mean and standard deviation
mean <- sum(face_values * face_counts) / sum(face_counts)
sd <- sqrt(sum((face_values - mean)^2 * face_counts) / sum(face_counts))
print(mean *100)
print(sd*100)

# normcdf - normal cumulative distribution function
# in R it is pnorm()
dist <- pnorm(270, mean *100 , sqrt(sd*100)) - pnorm(220, mean*100, sqrt(sd*100))
print(dist)
