# create matrix 4 by 4
m <- matrix(1:16, nrow = 4, ncol = 4)

# 1  = A
m[1, 1] <- 0 # A
m[1, 2] <- 1 # B
m[1, 3] <- 0 # C
m[1, 4] <- 0 # D

# 2 = B
m[2, 1] <- 0 # A
m[2, 2] <- 0 # B
m[2, 3] <- 1 # C
m[2, 4] <- 0 # D

# 3 = C
m[3, 1] <- 0 # A
m[3, 2] <- 1 # B
m[3, 3] <- 0 # C
m[3, 4] <- 1 # D

# 4 = D
m[4, 1] <- 0 # A
m[4, 2] <- 1 # B
m[4, 3] <- 0 # C
m[4, 4] <- 0 # D

# print matrix
m

# a^2
m %*% m

# nasobeni matice sousednosti sebou sama zjistime pocet sledu o delce 2 (mocnina == delka)
