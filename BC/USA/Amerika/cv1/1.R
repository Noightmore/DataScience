# compute binomial coefficient
# input: n, k
# output: binomial coefficient

binom <- function(n, k) {
  if (k > n) {
    return(0)
  }
  if (k == 0) {
    return(1)
  }
  if (k == n) {
    return(1)
  }
  return(binom(n - 1, k - 1) + binom(n - 1, k))
}

# call binom function
#binom(5, 3)
# print the result of binom function
binom(5, 3)
