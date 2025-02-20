# pr 22, vychazi z prikladu 21

#n over k function
nOverK <- function(n, k) {
  if (k == 0) {
    return(1)
  } else {
    return(n * nOverK(n - 1, k - 1) / k)
  }
}

# function
getPropability <- function() {
  sum <- 0
  for(i in 0:5){
    sum <- (sum + nOverK(15, 6-i) * nOverK(5, i) / nOverK(20, 6))
  }
  return(sum)
}

print(getPropability())

# pr 29:
# 15 chlapcu, 10 divek, vybirame 5 chlapcu a 5 divek
# kolik moznych kombinaci je?

# 15 over 5 times 10 over 5

# kombinatoricky pravidlo souctu: scitam 2  vice pravdebopodobnosti urcite sance ze se dej stane
#


# priklad 5 z jevu 2
# stastnych 10
# https://www.sazka.cz/loterie/stastnych-10/sazky-a-vysledky

getPropability2 <- function(){
    sum <- 0
    for(i in 0:10){
        sum <- sum + nOverK(10, i) * nOverK(70, 20-i) / nOverK(80, 20)
    }
    return(sum)
}

print(getPropability2())

# priklad 12 z jevu 2
# GEOMETRICKA PRAVDEPODOBNOST
# nutnost nakreslit :((
