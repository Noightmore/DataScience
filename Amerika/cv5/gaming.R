# diskretni rozdeleni
# - binomicke rozdeleni - pro nezavisle jevy
# (distribucni funkce spojite na intervalu - cdf;
# - Hustota pravdepodobnosti spojite na intervalue - pdf)

# binocdf - distribucni funkce binomickeho rozdeleni
# binopdf - pravdepodobnostni funkce binomickeho rozdeleni

# pravdepodobnostni funcke P(x = k) = n over k * pu^k * (1-pn)^(n-k)
# kde to prvni P ve vzorce je pravdepodobnost uspechu
# kde to druhe P ve vzorce je pravdepodobnost neuspechu

#p <- binpdf(2, 5, 0.5) prave dvakrat padne orel
#binocdf(4-1, 5, 0.5) alespon 4x padne orel


# binomial propability distribution function
binopdf <- function(k, n, p) {
  p <- choose(n, k) * p^k * (1-p)^(n-k)
  return(p)
}

# binomial cumulative distribution function
binocdf <- function(k, n, p) { # tohle je sus, nepouzivat
  p <- 0
  for (i in 0:k) {
    p <- p + binopdf(i, n, p)
  }
  return(p)
}

# pravdepodobnost, ze vyhraju ve sportce prvni cenu
# pravdepodobnost, ze vyhraju ve sportce prvni cenu je 1/13983816
# vsadim za rok 1000 krat a chci spocitat pravdepodobnost ze vyhraji prave 2 krat
p <- binopdf(2, 1000, 1/13983816)
#p

# pr 5b - pr a)
pz <- binopdf(3, 5, 0.8)
pz
# pz a pz_t jsou stejne
pz_t <- dbinom(3, 5, 0.8) # binopdf je to same co dbinom
pz_t

# pr 5b - pr b)
#pz2 <- (1 - binocdf(2.5, 5, 0.8))
#pz2
pz2_t <- (1 - pbinom(2.5, 5, 0.8)) # binocfd je to same co pbinom
pz2_t

#p2 <- binomcdf(2, 5, 0.8)

# bruh
# https://www.geeksforgeeks.org/binomial-distribution-in-r-programming/

# mnpdf - multinomial probability distribution function
# in R it is dmultinom()

# vypoctete pravdepodobnost ze z 32 karetniho balicku budou pri vyslosovani 3 karet prave 2 esa
# v tomto pripade esa nevracime do balicku
esa_pra <- dmultinom(c(2, 1), size = 3, prob = c(4/32, 28/32))
esa_pra

# hygepdf() - hypergeometric probability distribution function
# in R it is dhyper()

# geopdf() - geometric probability distribution function
# pravdepodobnost, ze padne orel pri 5. pokusu prave padne cislo 6 pri nahodnem nezavislem hazeni kostkou
# 4 krat nepadne s sanci 1/6 - na 5. pokus padne
# in R it is dgeom()
# geopdf(4, 1/6)

# geocdf - geometric cumulative distribution function

# distributor prodava knihu, 10 % knihkupcu ji koupi, jaka je pravdepodobnost, ze distributor bude poprve
# uspesny:
# a) prave u 5. navstevy knihkupectvi
a <- dgeom(4, 0.1) # geopdf(4, 0.1) matlab
a

# b) do 5. navstevy, 5. uz se nepocita
b <- pgeom(4-1, 0.1) # geocdf(4-1, 0.1) matlab
b

# c) pri osme a vice navsteve
c <- 1 - pgeom(7-1, 0.1) # 1 - geocdf(7-1, 0.1) matlab
c

# negativne binomicke rozdeleni

# pravdepodobnost vyskytu krevni skupiny A+ je 0.35. v nemocnici potrebuji najit 3 darce
# s touto krevni skupinou. Darcove vsak neznaji svoji krevni.
# jaka je pravdepodobnost, ze pro nalezeni prace 3. darce s krevni skupinou A+ budou muset vysetrit:
# a) prave 10 darcu
a2 <- dnbinom(7, 3, 0.35) # nbinpdf(7, 3, 0.35) matlab
a2 # 7 neuspesne, 3 uspesne

# b) vice jak 9 darcu
b2 <- 1 - pnbinom(6, 3, 0.35) # 1 - nbincdf(6, 3, 0.35) matlab
b2 # 6 neuspesnych, 3 uspesny

# c) aspon 6 (vcetne) a nejvyse 10 darcu (vcetne)
c2 <-  pnbinom(7, 3, 0.35)  - pnbinom(2, 3, 0.35)
c2 # tohle nevychazi a nikdo nevi proc

# poissonovo rozdeleni -> pokracovani mozna priste