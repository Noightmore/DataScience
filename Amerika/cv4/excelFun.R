library(readxl)

e <- read_excel("absolute-path-to-file") # .xlsx file
# priklad 26 3.* asi nekde
# zjistit stredni hodnotu

e <- as.numeric(unlist(e))

middleVal <- mean(e)
print(middleVal)

# get modus
#modus <- modus(e)
print(modus)

mediann <- median(e)
print(mediann)

# asi se podivat na to co to je quantil a quartil
q <- quantile(e)
print(q)
