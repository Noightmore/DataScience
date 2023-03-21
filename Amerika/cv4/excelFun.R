library(readxl)

# bruh no mode function in R :skull:
find_mode <- function(x) {
  u <- unique(x)
  tab <- tabulate(match(x, u))
  u[tab == max(tab)]
}

# print current working directory
#getwd()

e <- read_excel("Amerika/cv4/P0326.xlsx") # .xlsx file
# priklad 26 3.* asi nekde v trojce
# zjistit stredni hodnotu

e <- as.numeric(unlist(e))

middleVal <- mean(e)
print(middleVal)

# get modus
modus <- find_mode(e)
print(modus)

mediann <- median(e)
print(mediann)

# asi se podivat na to co to je quantil a quartil
q <- quantile(e)
print(q)

# rozptyl


