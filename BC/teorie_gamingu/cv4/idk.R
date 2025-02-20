
A <- matrix(nrow = 4, ncol = 4)
B <- matrix(nrow = 4, ncol = 3)


rownames(A) <- c("A", "B", "C", "D")
colnames(A) <- c("A", "B", "C", "D")

# create an identity matrix
I <- diag(4)

order_vec <- c(1, 3, 1, 1)

# filling of matrix A

# A
A[1, 1] <- 0 # A
A[1, 2] <- 1 # B
A[1, 3] <- 0 # C
A[1, 4] <- 0 # D

# B
A[2, 1] <- 1 # A
A[2, 2] <- 0 # B
A[2, 3] <- 1 # C
A[2, 4] <- 1 # D

# C
A[3, 1] <- 0 # A
A[3, 2] <- 1 # B
A[3, 3] <- 0 # C
A[3, 4] <- 0 # D

# D
A[4, 1] <- 0 # A
A[4, 2] <- 1 # B
A[4, 3] <- 0 # C
A[4, 4] <- 0 # D

# B matrix

# hrana a
B[1, 1] <- 1 # A
B[1, 2] <- 1 # B
B[1, 3] <- 0 # C
#B[1, 4] <- 0 # D

# hrana b
B[2, 1] <- 0 # A
B[2, 2] <- 1 # B
B[2, 3] <- 1 # C
#B[2, 4] <- 0 # D

# hrana c
B[3, 1] <- 0 # A
B[3, 2] <- 1 # B
B[3, 3] <- 1 # C
#B[3, 4] <- 0 # D

# hrana d
B[4, 1] <- 0 # A
B[4, 2] <- 1 # B
B[4, 3] <- 0 # C
#B[4, 4] <- 1 # D


# Laplas matrix
L <- (B %*% t(B))
print(L)
L2 <- I * order_vec
print(L2)


C <- matrix(c(1, 2, 4, 7, 6, 8, 8, 0), ncol = 2, byrow = TRUE)
#D <- (1:8, ncol = 2, nrow=4, byrow = TRUE)
print(C)
